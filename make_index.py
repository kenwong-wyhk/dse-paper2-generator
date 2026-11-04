#!/usr/bin/env python3
"""
Assemble the student app: inject question metadata into app_template.html.

Produces index.html next to a questions/ folder of pre-rendered SVGs.
Run build_app.py first to render the SVGs.
"""

import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIPE = os.path.join(ROOT, '0 Pipeline')

classified = json.load(open(os.path.join(PIPE, 'questions_classified.json'), encoding='utf-8'))
YEARS = sorted({r['year'] for r in classified})

# the empirical topic profile of every slot — this is what keeps a mock looking real
slot_dist = {}
for n in range(1, 46):
    c = Counter(r['code'] for r in classified if r['no'] == n)
    slot_dist[n] = dict(c)

questions = []
missing = []
for r in sorted(classified, key=lambda z: (z['year'], z['no'])):
    qid = f"{r['year']}-{r['no']:02d}"
    if not os.path.exists(os.path.join(HERE, 'questions', qid + '.svg')):
        missing.append(qid)
        continue
    questions.append({
        'id': qid,
        'y': int(r['year']),
        'q': r['no'],
        't': r['code'],
        's': r['section'],
        'a': r['answer'],
    })

data = {'questions': questions, 'slotDist': slot_dist}

tpl = open(os.path.join(HERE, 'app_template.html'), encoding='utf-8').read()
if '/*__DATA__*/' not in tpl:
    raise SystemExit('template placeholder /*__DATA__*/ not found')
html = tpl.replace('/*__DATA__*/', json.dumps(data, separators=(',', ':')))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)

print(f'questions embedded: {len(questions)}')
if missing:
    print(f'missing SVGs ({len(missing)}):', missing[:10])
print(f'index.html: {len(html)/1e6:.2f} MB')
