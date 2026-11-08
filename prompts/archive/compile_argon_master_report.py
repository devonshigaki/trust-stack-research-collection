#!/usr/bin/env python3
import os
import json

reviews_dir = '/Users/devonshigaki/Desktop/Research/reviews'
papers = ['DOCAS', 'GTT', 'TFP', 'WHITEPAPER']
results = {}

for p in papers:
    with open(os.path.join(reviews_dir, f'ARGON4_DARRELL_HUFF_{p}.json')) as f:
        results[p] = json.load(f)

report = """# GEMINI 4 ARGON DETERMINISTIC AUDIT REPORT
**Evaluation Standard:** Darrell Huff's 5-Question Framework (`Score Academic Paper Prompt.rtf`)  
**Evaluator Model:** `gemini-4-argon` (Google GenAI SDK; Temperature: 0.0)  
**Date of Audit:** November 7, 2026  

---

## EXECUTIVE SUMMARY TABLE (GEMINI 4 ARGON RAW EVALUATION)

```
========================================================================================================================
                              GEMINI 4 ARGON DARRELL HUFF AUDIT SCORECARD (100 PTS)
========================================================================================================================
Paper Key & Title                       | Q1: Who Says? | Q2: How Know? | Q3: Missing?  | Q4: Subject?  | Q5: Sense?    | Total Score
----------------------------------------+---------------+---------------+---------------+---------------+---------------+------------
"""

for name in papers:
    data = results[name]
    cat = data.get('category_scores', {})
    q1 = cat.get('who_says_so', {}).get('score', 0)
    q2 = cat.get('how_does_researcher_know', {}).get('score', 0)
    q3 = cat.get('whats_missing', {}).get('score', 0)
    q4 = cat.get('did_someone_change_subject', {}).get('score', 0)
    q5 = cat.get('does_it_make_sense', {}).get('score', 0)
    total = data.get('total_score', 0)
    verdict = data.get('verdict', '')
    report += f"{name:<39} | {q1}/20         | {q2}/20         | {q3}/20         | {q4}/20         | {q5}/20         | {total}/100 ({verdict})\n"

report += """========================================================================================================================
```

---

## ITEMIZED AUDIT DETAILS BY PAPER

"""

for name in papers:
    report += f"### {name} Evaluation Output\n```json\n"
    report += json.dumps(results[name], indent=2)
    report += "\n```\n\n"

with open(os.path.join(reviews_dir, 'ARGON4_DARRELL_HUFF_MASTER_REPORT.md'), 'w') as f:
    f.write(report)

print("Updated ARGON4_DARRELL_HUFF_MASTER_REPORT.md successfully!")
