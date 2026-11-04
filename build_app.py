#!/usr/bin/env python3
"""
Build a standalone, shareable mock-paper app for students.

Students have no Python and no LaTeX, so the paper must be generated in the browser.
That means each question is pre-rendered once, here, from LaTeX into a vector SVG.
The app then just picks 45 of them and prints.

Pipeline per question:  LaTeX block -> standalone .tex -> pdflatex -> PDF -> SVG
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SAMPLE = os.path.join(ROOT, 'Paper 2 Sample')
OUT_Q = os.path.join(HERE, 'questions')

WRAP = r"""\documentclass[border=4pt]{standalone}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{mathptmx}
\usepackage{microtype}

\usepackage{tikz}
\usetikzlibrary{calc,angles,quotes,intersections,patterns,decorations.markings}
\providecommand{\wideparen}[1]{\widehat{#1}}
\renewcommand{\labelenumi}{\Alph{enumi}.}
\newenvironment{choices}{\begin{enumerate}}{\end{enumerate}}
\newcommand{\choice}{\item}
\let\correctchoice\choice
\begin{document}
\begin{minipage}{168mm}
%%Q%%
\end{minipage}
\end{document}
"""

STRUCT = re.compile(
    r'(\\newpage|\\clearpage|\\section\*\{Section [AB]\}'
    r'|\\end\{questions\}|\\begin\{questions\}|\\setcounter\{question\}\{\d+\})\s*$')


def load_blocks():
    """{(year, qno): latex block} with solutions and structural commands stripped."""
    out = {}
    for f in os.listdir(SAMPLE):
        m = re.match(r'(\d{4}) P2\.tex$', f)
        if not m:
            continue
        yr = m.group(1)
        src = open(os.path.join(SAMPLE, f), encoding='utf-8').read()
        end = src.find('\\end{questions}')
        body = src[:end] if end > 0 else src
        for i, p in enumerate(re.split(r'\\question\b', body)[1:], 1):
            p = p.rstrip()
            p = re.sub(r'(\s*%[^\n]*)+$', '', p).rstrip()
            while True:
                q = STRUCT.sub('', p).rstrip()
                if q == p:
                    break
                p = q
            p = re.sub(r'\\begin\{solution\}.*?\\end\{solution\}', '', p, flags=re.S)
            p = p.replace('\\textwidth', '\\linewidth')
            out[(yr, i)] = p
    return out


def render_one(job):
    year, qno, block = job
    key = f'{year}-{qno:02d}'
    svg_path = os.path.join(OUT_Q, key + '.svg')
    if os.path.exists(svg_path):
        return key, 'cached'

    with tempfile.TemporaryDirectory() as td:
        tex = os.path.join(td, 'q.tex')
        open(tex, 'w', encoding='utf-8').write(WRAP.replace('%%Q%%', block))
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'q.tex'],
                           cwd=td, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pdf = os.path.join(td, 'q.pdf')
        if r.returncode != 0 or not os.path.exists(pdf):
            return key, 'latex-failed'
        try:
            import pymupdf
            doc = pymupdf.open(pdf)
            svg = doc[0].get_svg_image(text_as_path=True)
            # browsers read a unitless SVG width as CSS pixels; give it real mm
            # so the natural size matches the printed page (1pt = 25.4/72 mm)
            def to_mm(m):
                w, h = float(m.group(1)), float(m.group(2))
                return f'width="{w*25.4/72:.1f}mm" height="{h*25.4/72:.1f}mm"'
            svg = re.sub(r'width="([\d.]+)" height="([\d.]+)"', to_mm, svg, count=1)
            open(svg_path, 'w', encoding='utf-8').write(svg)
            return key, 'ok'
        except Exception as e:
            return key, f'svg-failed: {e}'


def main():
    os.makedirs(OUT_Q, exist_ok=True)
    blocks = load_blocks()
    jobs = [(int(y), n, b) for (y, n), b in sorted(blocks.items())]
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if limit:
        jobs = jobs[:limit]

    print(f'rendering {len(jobs)} questions...')
    results = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for i, res in enumerate(ex.map(render_one, jobs), 1):
            results.append(res)
            if i % 50 == 0:
                print(f'  {i}/{len(jobs)}')

    from collections import Counter
    tally = Counter(r for _, r in results)
    print('\nresults:')
    for k, v in tally.most_common():
        print(f'  {k:24s} {v}')
    bad = [k for k, r in results if r not in ('ok', 'cached')]
    if bad:
        print('\nfailed:', bad[:20])
        json.dump(bad, open(os.path.join(HERE, 'render_failures.json'), 'w'))
    total = sum(os.path.getsize(os.path.join(OUT_Q, f))
                for f in os.listdir(OUT_Q) if f.endswith('.svg'))
    print(f'\nSVG total: {total/1e6:.1f} MB in {len(os.listdir(OUT_Q))} files')


if __name__ == '__main__':
    main()
