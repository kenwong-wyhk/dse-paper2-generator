# Mock Paper Generator

A one-click practice-paper generator for HKDSE Mathematics (Compulsory Part) Paper 2.

## How to use it

1. Unzip the folder somewhere on your computer.
2. Double-click **`index.html`**. It opens in your browser.
3. Press **Generate new paper**.
4. Press **Print / Save as PDF** and choose "Save as PDF" to keep it.

That's it. Nothing to install.

## What it does

Every paper is 45 multiple-choice questions drawn at random from a bank of
**14 years of real HKDSE Paper 2** (2012–2025, 630 questions), plus any extra practice
questions added since. Each question keeps the position and topic where it
belongs, so the paper has the same shape as the real thing:

- **Section A (Q1–Q30)** — algebra, geometry, mensuration, coordinate geometry, statistics
- **Section B (Q31–Q45)** — logarithms, complex numbers, linear programming, 3-D trigonometry,
  permutations, probability, dispersion

No two papers are the same, so you can generate as many as you like.

No topic appears more often than it ever did in a real paper — for example at most two
polynomial questions, and at most one on the factor theorem — so a paper never turns into
three variations of the same question.

The answer key is always distributed like the real paper, but the letters move around:
**Section A is always two 7s and two 8s** (for example 8/7/8/7, or 7/8/8/7, or 7/7/8/8),
and **Section B is always one 3 and three 4s**. Which letter gets the larger count is
reshuffled for every paper, so there is no pattern to spot. You can see the counts in the
top-right corner after generating.

## AI questions

Some questions are written as variations of past-paper questions — same structure and same
method, different numbers. They are marked with a small **AI** badge next to the question
number, and the **Include AI questions** box in the toolbar lets you leave them out.

## The buttons

| Button | What it does |
|---|---|
| **Generate new paper** | Builds a fresh paper. Press it again for another one. |
| **Full paper / Section A only / Section B only** | Choose how much to practise. Section A only is good for a 45-minute drill. |
| **Print / Save as PDF** | Opens the print dialog. Choose "Save as PDF" to keep a copy. |
| **Show answers** | Reveals the answer key at the end of the paper. It is hidden by default, and hidden in the printout unless you show it first. |

## Tips

- **Do Section A first, timed.** 30 questions in 45 minutes. That is the pace the real exam
  expects — 75 minutes for the whole paper.
- **Do not peek at the key.** Generate the paper, print it, then close the tab. The key is
  only shown when you press the button.
- **If a paper feels too hard**, generate another. Difficulty varies slightly between papers
  because the questions are real ones, not written to a template.
- **Working matters more than the answer.** Paper 2 is multiple choice, but the skills it
  tests are the same ones Paper 1 marks for method.

## Technical notes

- Works in any modern browser — Chrome, Safari, Edge, Firefox. No internet needed.
- Every question is a vector image, so it prints sharply at any size.
- The whole folder is about 30 MB. Keep `index.html` and the `questions` folder together;
  the app will not work if they are separated.
- On a phone or tablet it works, but printing is easier from a computer.
