#!/usr/bin/env python3
"""
Evaluate The Trust Stack Papers using Gemini 4 Argon & Darrell Huff's Framework
Invokes the Google GenAI SDK (gemini-4-argon) at temperature 0.0 with the exact
criteria from 'Score Academic Paper Prompt.rtf'.
"""

import os
import re
import json
import time
from google import genai
from google.genai import types

BASE_DIR = "/Users/devonshigaki/Desktop/Research"
PAPERS_DIR = os.path.join(BASE_DIR, "papers")
REVIEWS_DIR = os.path.join(BASE_DIR, "reviews")
PROMPT_RTF = os.path.join(BASE_DIR, "Score Academic Paper Prompt.rtf")

client = genai.Client()

def extract_text_from_rtf(rtf_path):
    with open(rtf_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # Remove RTF control sequences
    text = re.sub(r'\\[a-z0-9\-]+ ?', ' ', content)
    text = re.sub(r'[{}]', '', text)
    text = text.replace('\\\'97', '—')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def evaluate_paper_argon(paper_name, paper_path, system_prompt):
    print(f"\n🚀 Invoking Gemini 4 Argon for: {paper_name}...")
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()

    user_content = f"""
PAPER TITLE: {paper_name}

=== BEGIN PAPER TEXT ===
{paper_text}
=== END PAPER TEXT ===

Now evaluate the paper above strictly following Darrell Huff's 5-Question Framework.
Ensure deterministic output in the required JSON format.
"""

    config = types.GenerateContentConfig(
        temperature=0.0,
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )

    t0 = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-4-argon",
            contents=user_content,
            config=config
        )
        elapsed = time.time() - t0
        print(f"✓ Gemini 4 Argon completed evaluation in {elapsed:.1f}s")
        return response.text
    except Exception as e:
        print(f"Error calling Gemini 4 Argon: {e}")
        # Fallback to standard text call without json mime type if model complains
        config.response_mime_type = None
        response = client.models.generate_content(
            model="gemini-4-argon",
            contents=user_content,
            config=config
        )
        return response.text

def main():
    print("=" * 80)
    print("EXECUTING LIVE GEMINI 4 ARGON EVALUATION (DARRELL HUFF FRAMEWORK)")
    print("=" * 80)

    system_prompt = extract_text_from_rtf(PROMPT_RTF)
    print(f"Extracted Framework System Prompt ({len(system_prompt)} chars)")

    papers = [
        ("DOCAS", os.path.join(PAPERS_DIR, "docas.md")),
        ("GTT", os.path.join(PAPERS_DIR, "gtt.md")),
        ("TFP", os.path.join(PAPERS_DIR, "tfp.md")),
        ("Whitepaper", os.path.join(PAPERS_DIR, "whitepaper.md"))
    ]

    results = {}
    for name, path in papers:
        res_json_str = evaluate_paper_argon(name, path, system_prompt)
        
        # Save individual raw JSON
        out_json_path = os.path.join(REVIEWS_DIR, f"ARGON4_DARRELL_HUFF_{name.upper()}.json")
        with open(out_json_path, "w", encoding="utf-8") as f:
            f.write(res_json_str)
        print(f"Saved: {out_json_path}")
        
        try:
            parsed = json.loads(res_json_str)
            results[name] = parsed
        except Exception:
            # Extract JSON block if wrapped in markdown
            match = re.search(r'\{.*\}', res_json_str, re.DOTALL)
            if match:
                results[name] = json.loads(match.group(0))
            else:
                results[name] = {"raw": res_json_str}

    # Generate Master Markdown Report
    summary_md = f"""# GEMINI 4 ARGON DETERMINISTIC AUDIT REPORT
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
    for name in ["DOCAS", "GTT", "TFP", "Whitepaper"]:
        data = results.get(name, {})
        cat = data.get("category_scores", {})
        q1 = cat.get("who_says_so", {}).get("score", "N/A")
        q2 = cat.get("how_does_researcher_know", {}).get("score", "N/A")
        q3 = cat.get("whats_missing", {}).get("score", "N/A")
        q4 = cat.get("did_someone_change_subject", {}).get("score", "N/A")
        q5 = cat.get("does_it_make_sense", {}).get("score", "N/A")
        total = data.get("total_score", "N/A")
        verdict = data.get("verdict", "")
        summary_md += f"{name:<39} | {q1}/20         | {q2}/20         | {q3}/20         | {q4}/20         | {q5}/20         | {total}/100 ({verdict})\n"

    summary_md += """========================================================================================================================
```

---

## ITEMIZED AUDIT DETAILS BY PAPER

"""
    for name in ["DOCAS", "GTT", "TFP", "Whitepaper"]:
        summary_md += f"### {name} Evaluation Output\n```json\n"
        summary_md += json.dumps(results.get(name, {}), indent=2)
        summary_md += "\n```\n\n"

    master_report_path = os.path.join(REVIEWS_DIR, "ARGON4_DARRELL_HUFF_MASTER_REPORT.md")
    with open(master_report_path, "w", encoding="utf-8") as f:
        f.write(summary_md)

    print(f"\n🎉 Successfully compiled Master Report: {master_report_path}")

if __name__ == "__main__":
    main()
