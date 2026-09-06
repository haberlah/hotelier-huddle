#!/usr/bin/env python3
"""
Compiles the complete Hotelier Huddle corpus (index, glossary, panels, questions,
transcripts, and pre-indexed turns) into a single JSON artifact for the Cloudflare Worker.
"""

import os
import json
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def bundle():
    corpus = {
        "index": {},
        "glossary_raw": "",
        "glossary_terms": [],
        "panels": {},
        "questions": {},
        "transcripts": {},
        "turns": []
    }

    # 1. Index
    idx_path = os.path.join(BASE_DIR, "index.json")
    with open(idx_path, 'r', encoding='utf-8') as f:
        corpus["index"] = json.load(f)

    # 2. Glossary
    gloss_path = os.path.join(BASE_DIR, "HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md")
    with open(gloss_path, 'r', encoding='utf-8') as f:
        glossary_text = f.read()
        corpus["glossary_raw"] = glossary_text

    for line in glossary_text.splitlines():
        m = re.match(r'\|\s*\*\*([^*]+?)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|\n]+)\|', line)
        if m:
            corpus["glossary_terms"].append({
                "term": m.group(1).strip(),
                "aliases_or_mishearings": m.group(2).strip(),
                "definition": m.group(3).strip(),
                "strategic_context": m.group(4).strip()
            })

    # 3. Panels
    panel_map = {
        "commercial_alignment": "PANEL_01_Commercial_Alignment_Sales_vs_Revenue.md",
        "ai_technology": "PANEL_02_AI_Technology_and_the_Human_Touch.md",
        "crisis_resilience": "PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience.md",
        "modern_leadership": "PANEL_04_Leadership_Culture_and_People_Over_Profit.md",
        "nonlinear_careers": "PANEL_05_Non_Linear_Careers_and_Boardroom_Skills.md",
        "asset_strategy": "PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy.md",
        "service_craft": "PANEL_07_Frontline_Guest_Experience_and_Service_Craft.md"
    }

    for cid, fname in panel_map.items():
        p = os.path.join(BASE_DIR, "derived_knowledge_base", "virtual_panels", fname)
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                corpus["panels"][cid] = f.read()

    # 4. Questions
    q_files = glob.glob(os.path.join(BASE_DIR, "derived_knowledge_base", "question_knowledge_bases", "*.md"))
    for qf in q_files:
        qid = os.path.basename(qf).split("_")[1].lower()
        with open(qf, 'r', encoding='utf-8') as f:
            corpus["questions"][qid] = f.read()

    # 5. Transcripts and turns
    ep_by_num = {ep["episode_number"]: ep for ep in corpus["index"].get("episodes", [])}
    for path in sorted(glob.glob(os.path.join(BASE_DIR, "transcripts", "*.md"))):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        m_num = re.search(r'episode_number:\s*(\d+)', content)
        if m_num:
            ep_num = int(m_num.group(1))
        else:
            ep_num = int(os.path.basename(path)[:2])
            
        corpus["transcripts"][str(ep_num)] = content
        ep_info = ep_by_num.get(ep_num, {})
        
        for line in content.splitlines():
            m_turn = re.match(r'^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(?:\*\*([^*]+?):\*\*)?\s*(.+)$', line.strip())
            if m_turn:
                ts, spk, text = m_turn.groups()
                spk = spk or "Speaker"
                corpus["turns"].append({
                    "episode_number": ep_num,
                    "episode_title": ep_info.get("title", ""),
                    "guest": ep_info.get("guest", ""),
                    "tags": ep_info.get("tags", []),
                    "timestamp": ts,
                    "speaker": spk,
                    "text": text
                })

    out_dir = os.path.join(BASE_DIR, "cloudflare_worker", "src")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "corpus.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False)

    sz = os.path.getsize(out_path)
    print(f"Successfully compiled {out_path} ({sz:,} bytes / {sz/1024/1024:.2f} MB).")

if __name__ == "__main__":
    bundle()
