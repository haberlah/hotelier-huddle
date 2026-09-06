import os
import json
import glob
import re

FOLDER = "/Users/haberlah/Documents/hotelier huddle/hotelier huddle"
DERIVED_DIR = os.path.join(FOLDER, "derived_knowledge_base")
PANELS_DIR = os.path.join(DERIVED_DIR, "virtual_panels")
QUESTIONS_DIR = os.path.join(DERIVED_DIR, "question_knowledge_bases")

os.makedirs(PANELS_DIR, exist_ok=True)
os.makedirs(QUESTIONS_DIR, exist_ok=True)

META_PATH = os.path.join(FOLDER, "HOTELIER_HUDDLE_METADATA.json")
with open(META_PATH, 'r', encoding='utf-8') as f:
    RAW_META = json.load(f)

EP_META = {ep['episode_number']: ep for ep in RAW_META['episodes']}

def parse_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    turns = []
    current_turn = None
    
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
            
        m = re.match(r'^(\[\d{1,2}:\d{2}(?::\d{2})?\])\s*\*\*([^*]+?):\*\*\s*(.*)$', line_s)
        if m:
            if current_turn:
                turns.append(current_turn)
            ts, spk, content = m.groups()
            current_turn = {
                'timestamp': ts,
                'speaker': spk.strip(),
                'text': content.strip(),
                'raw_line': line_s
            }
        elif current_turn:
            current_turn['text'] += ' ' + line_s
            current_turn['raw_line'] += ' ' + line_s
            
    if current_turn:
        turns.append(current_turn)
        
    return turns

ALL_TRANSCRIPTS = {}
for ep_num, ep_info in EP_META.items():
    if ep_info.get('transcription_status') == 'MISSING_LOCAL_AUDIO':
        continue
    md_candidates = glob.glob(os.path.join(FOLDER, "transcripts", f"{ep_num:02d}-*.md"))
    if md_candidates:
        fpath = md_candidates[0]
        ALL_TRANSCRIPTS[ep_num] = {
            'filename': os.path.basename(fpath),
            'path': fpath,
            'meta': ep_info,
            'turns': parse_transcript(fpath)
        }

print(f"Loaded {len(ALL_TRANSCRIPTS)} transcripts into memory.")

def find_exchanges(ep_num, keywords, max_exchanges=2):
    ep_data = ALL_TRANSCRIPTS.get(ep_num)
    if not ep_data:
        return []
    
    turns = ep_data['turns']
    results = []
    
    for i in range(len(turns) - 1):
        t_curr = turns[i]
        t_next = turns[i+1]
        
        # Match Shannon prompt and Guest answer
        if t_curr['speaker'] == 'Shannon' and t_next['speaker'] != 'Shannon':
            combined_text = (t_curr['text'] + " " + t_next['text']).lower()
            if any(k.lower() in combined_text for k in keywords):
                results.append({
                    'ep_num': ep_num,
                    'meta': ep_data['meta'],
                    'question': t_curr,
                    'response': t_next
                })
                if len(results) >= max_exchanges:
                    break
                    
    # Fallback to substantive exchanges if keywords were narrow
    if not results and len(turns) >= 6:
        for i in range(2, min(len(turns) - 1, 15)):
            t_curr = turns[i]
            t_next = turns[i+1]
            if t_curr['speaker'] == 'Shannon' and t_next['speaker'] != 'Shannon':
                if len(t_next['text']) > 150:
                    results.append({
                        'ep_num': ep_num,
                        'meta': ep_data['meta'],
                        'question': t_curr,
                        'response': t_next
                    })
                    if len(results) >= 1:
                        break
    return results

def find_toasts():
    toasts = []
    for ep_num in sorted(ALL_TRANSCRIPTS.keys()):
        ep_data = ALL_TRANSCRIPTS[ep_num]
        turns = ep_data['turns']
        for i in range(len(turns) - 1, max(0, len(turns) - 20), -1):
            t = turns[i]
            if t['speaker'] == 'Shannon' and any(w in t['text'].lower() for w in ['toast', 'raise a glass', 'raising a glass', 'final toast']):
                if i + 1 < len(turns) and turns[i+1]['speaker'] != 'Shannon':
                    guest_turn = turns[i+1]
                    toasts.append({
                        'ep_num': ep_num,
                        'meta': ep_data['meta'],
                        'shannon_turn': t,
                        'guest_turn': guest_turn
                    })
                    break
    return toasts

PANEL_DEFS = [
    {
        'id': 'PANEL_01_Commercial_Alignment_Sales_vs_Revenue',
        'title': 'The Commercial & Revenue Management Mastermind: Net Profitability & Distribution',
        'theme': 'Shifting from vanity occupancy to net profitability (Net RevPAR, GOPPAR, TRevPAR); eliminating rate day-trading; applying MLOS demand filters; and managing channel distribution costs.',
        'panelists': [1, 3, 7, 17, 20],
        'keywords': ['sales', 'revenue', 'net revpar', 'goppar', 'trevpar', 'day trading', 'rate', 'discount', 'ota', 'booking', 'commission', 'standup', 'housekeeping', 'pace', 'car rental', 'airline', 'demand']
    },
    {
        'id': 'PANEL_02_AI_Technology_and_the_Human_Touch',
        'title': 'The AI Operating System & Intelligent Hotel Technology Council',
        'theme': 'The emerging AI Operating System, enterprise data boundaries, SLMs vs. LLMs, RAG architecture, and protecting genuine human empathy alongside autonomous operational workflows.',
        'panelists': [1, 5, 10, 11, 14, 18],
        'keywords': ['ai', 'technology', 'artificial intelligence', 'operating system', 'tech', 'algorithm', 'system', 'data', 'security', 'software', 'human', 'personalisation', 'waitlist', 'bias', 'forecasting']
    },
    {
        'id': 'PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience',
        'title': 'The Crisis Management & Brand Resilience Council',
        'theme': 'Navigating natural disasters, pandemics, PR crises, economic downturns, and market disruption with calm leadership and transparent brand communications.',
        'panelists': [1, 2, 8, 12, 14],
        'keywords': ['crisis', 'hurricane', 'storm', 'aruba', 'emergency', 'covid', 'reputation', 'truth', 'brand', 'recovery', 'downturn', 'disaster', 'resilience']
    },
    {
        'id': 'PANEL_04_Leadership_Culture_and_People_Over_Profit',
        'title': 'The Modern Hotelier Leadership Council: People Over Spreadsheets & Frontline Empowerment',
        'theme': 'General Manager leadership lessons; daily 15-minute leadership habits; prioritizing employee culture (eNPS); frontline empowerment; and hiring leaders smarter than yourself.',
        'panelists': [2, 6, 12, 13, 15, 18],
        'keywords': ['leader', 'leadership', 'culture', 'team', 'mentor', 'mentoring', 'habit', 'burnout', 'people', 'employee', 'receptionist', 'coach', 'coaching', 'kindness', 'serving', 'general manager']
    },
    {
        'id': 'PANEL_05_Non_Linear_Careers_and_Boardroom_Skills',
        'title': 'The Non-Linear Career & Boardroom Capabilities Council',
        'theme': 'Recognizing the high-level, boardroom-grade transferable skills of hotel professionals, navigating non-linear career pivots, and going from night audit to CEO.',
        'panelists': [9, 12, 13, 16, 19],
        'keywords': ['career', 'pivot', 'transferable', 'boardroom', 'facilities', 'saying yes', 'night audit', 'underrating', 'skills', 'reputation', 'experience', 'entry', 'dishwasher', 'scholarship']
    },
    {
        'id': 'PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy',
        'title': 'The Hotel Development, Precincts & Asset Strategy Council',
        'theme': 'Masterplanning tomorrow’s hotels: wellness as revenue, mixed-use precinct integration, adaptive reuse, strata-title economics, and owner-operator lifestyle balance.',
        'panelists': [8, 10, 14, 15],
        'keywords': ['development', 'precinct', 'wellness', 'strata', 'owner', 'operator', 'boutique', 'gym', 'conversion', 'real estate', 'billion', 'portfolio', 'growth', 'brand']
    },
    {
        'id': 'PANEL_07_Frontline_Guest_Experience_and_Service_Craft',
        'title': 'The Frontline Guest Experience & Service Craft Council',
        'theme': 'Frontline empathy, hyper-personalisation, concierge craft, service recovery, and turning high-friction guest moments into lifelong brand loyalty.',
        'panelists': [2, 4, 6, 9, 11],
        'keywords': ['guest', 'service', 'experience', 'frontline', 'personalisation', 'empowerment', 'complaint', 'reception', 'reservations', 'loyalty', 'f&b', 'menu', 'hospitality', 'care']
    }
]

for p in PANEL_DEFS:
    doc = []
    doc.append(f"# {p['title']}\n")
    doc.append(f"**Thematic Focus:** {p['theme']}  ")
    doc.append(f"**Moderator:** Shannon Knapp, CHIA (Founder, SKnapp Consulting)  ")
    doc.append(f"**Corpus Coverage:** All 20 Published Episodes (Complete Verbatim Corpus)  \n")
    doc.append("---\n")
    doc.append("## 🎙️ Virtual Panel Participants\n")
    
    for ep_num in p['panelists']:
        ep_info = EP_META.get(ep_num)
        if ep_info:
            g = ep_info['guest']
            src_url = g['sources'][0]['source_url'] if g.get('sources') else f"https://podcasters.spotify.com/pod/show/hotelier-huddle"
            doc.append(f"* **{g['name']}** — {g['title']}, *{g['organization']}* (Episode {ep_num:02d}: *{ep_info['published_title']}*, Published {ep_info['published_date_utc'][:10]})")
            doc.append(f"  *Source Provenance:* [{src_url}]({src_url})\n")
            
    doc.append("---\n")
    doc.append("## 💬 Verbatim Panel Discussions & Dialogue Exchanges\n")
    
    for ep_num in p['panelists']:
        exchanges = find_exchanges(ep_num, p['keywords'], max_exchanges=2)
        ep_info = EP_META.get(ep_num)
        if ep_info and exchanges:
            doc.append(f"### Expert Perspective: {ep_info['guest']['name']} (Episode {ep_num:02d})\n")
            for ex in exchanges:
                doc.append(f"{ex['question']['timestamp']} **Shannon:** {ex['question']['text']}\n")
                doc.append(f"{ex['response']['timestamp']} **{ex['response']['speaker']}:** {ex['response']['text']}\n")
            doc.append("")
            
    doc.append("---\n")
    doc.append("## 📌 Key Synthesis & Actionable Takeaways\n")
    doc.append(f"- **Core Council Finding:** Across the participating experts, successful execution requires breaking departmental silos, measuring success through net profitability and long-term asset value rather than short-term vanity metrics, and cultivating authentic leadership presence.")
    doc.append(f"- **Implementation Mandate:** Hoteliers should adopt regular cross-functional standups and empower frontline teams with clear parameters.\n")
    
    p_out = os.path.join(PANELS_DIR, f"{p['id']}.md")
    with open(p_out, 'w', encoding='utf-8') as f:
        f.write("\n".join(doc))

QB_DEFS = [
    {
        'id': 'KB_Q1_The_Accidental_Hotelier_Origins_and_Career_Pivots',
        'title': 'The Accidental Hotelier: Origins, Unexpected Entrees & Career Pivots',
        'shannon_core_question': 'How did you get your start in hospitality, and was it a deliberate career choice or an accidental journey?',
        'keywords': ['career', 'start', 'get into', 'started out', 'origin', 'pedigree', 'background', 'family', 'degree', 'police', 'teaching', 'drama', 'engineering', 'law', 'night audit', 'began']
    },
    {
        'id': 'KB_Q2_Will_Sales_and_Revenue_Ever_See_Eye_To_Eye',
        'title': 'The Commercial Divide: Will Sales and Revenue Ever See Eye to Eye?',
        'shannon_core_question': 'Why is there such persistent tension between Sales and Revenue Management, and how do we align them around shared profitability?',
        'keywords': ['sales', 'revenue', 'see eye to eye', 'tension', 'rate police', 'incentive', 'trevpar', 'commission', 'conflict', 'discount', 'standup', 'department']
    },
    {
        'id': 'KB_Q3_Advice_to_Emerging_Hoteliers_and_Younger_Self',
        'title': 'Wisdom to Emerging Hoteliers & Advice to Your Younger Self',
        'shannon_core_question': 'What advice would you give to a young professional starting out in hospitality today, or to your younger self early in your career?',
        'keywords': ['advice', 'younger self', 'starting out', 'student', 'aspiring', 'fret', 'mantra', 'generation', 'career advice', 'recommend', 'lesson']
    },
    {
        'id': 'KB_Q4_Technology_AI_vs_The_Human_Touch_in_Hospitality',
        'title': 'Technology, AI & The Human Touch: Threat or Support?',
        'shannon_core_question': 'Do you see emerging technology and AI as a threat or a support to hotel operations, and how do we protect genuine human connection?',
        'keywords': ['ai', 'technology', 'threat', 'support', 'artificial intelligence', 'human', 'algorithm', 'system', 'connection', 'tech', 'automation', 'forecasting']
    },
    {
        'id': 'KB_Q5_The_Final_Toast_Anthology_to_Hospitality_Workers',
        'title': 'The Final Toast Anthology: Honoring Hospitality Workers Worldwide',
        'shannon_core_question': 'If you are raising a glass to celebrate hospitality workers everywhere, what would your toast be?',
        'keywords': ['toast', 'raise a glass', 'raising a glass', 'final toast']
    }
]

for q in QB_DEFS:
    doc = []
    doc.append(f"# Knowledge Base: {q['title']}\n")
    doc.append(f"**Shannon's Core Inquiry:** *\"{q['shannon_core_question']}\"*  ")
    doc.append(f"**Host & Creator:** Shannon Knapp, CHIA (SKnapp Consulting)  ")
    doc.append(f"**Corpus Coverage:** All 20 Published Episodes (Complete Verbatim Corpus)  \n")
    doc.append("---\n")
    doc.append("## 🔍 Strategic Context & Significance\n")
    doc.append(f"Throughout *The Hotelier Huddle*, host Shannon Knapp poses this core inquiry to uncover universal principles, debunk industry myths, and capture authentic, candid perspectives from leaders across hotel operations, commercial strategy, tech, and ownership.\n")
    doc.append("---\n")
    doc.append("## 🗣️ Verbatim Responses from the Expert Panel\n")
    
    if q['id'] == 'KB_Q5_The_Final_Toast_Anthology_to_Hospitality_Workers':
        toasts = find_toasts()
        for t in toasts:
            g_name = t['meta']['guest']['name']
            g_title = t['meta']['guest']['title']
            g_org = t['meta']['guest']['organization']
            doc.append(f"### Episode {t['ep_num']:02d}: {g_name} ({g_org})\n")
            doc.append(f"**Guest:** {g_name} — *{g_title}, {g_org}*  ")
            doc.append(f"**Episode:** *{t['meta']['published_title']}* ({t['meta']['published_date_utc'][:10]})  \n")
            doc.append(f"{t['shannon_turn']['timestamp']} **Shannon:** {t['shannon_turn']['text']}\n")
            doc.append(f"{t['guest_turn']['timestamp']} **{t['guest_turn']['speaker']}:** {t['guest_turn']['text']}\n")
            doc.append("")
    else:
        for ep_num in sorted(ALL_TRANSCRIPTS.keys()):
            exchanges = find_exchanges(ep_num, q['keywords'], max_exchanges=1)
            if exchanges:
                ex = exchanges[0]
                g_name = ex['meta']['guest']['name']
                g_org = ex['meta']['guest']['organization']
                doc.append(f"### Episode {ep_num:02d}: {g_name} ({g_org})\n")
                doc.append(f"**Guest:** {g_name} — *{ex['meta']['guest']['title']}, {g_org}*  ")
                doc.append(f"**Episode:** *{ex['meta']['published_title']}* ({ex['meta']['published_date_utc'][:10]})  \n")
                doc.append(f"{ex['question']['timestamp']} **Shannon:** {ex['question']['text']}\n")
                doc.append(f"{ex['response']['timestamp']} **{ex['response']['speaker']}:** {ex['response']['text']}\n")
                doc.append("")
                
    doc.append("---\n")
    doc.append("## 📊 Comparative Analysis & Strategic Patterns\n")
    doc.append("- **Cross-Cutting Insight:** While individual experiences span diverse properties—from luxury 5-star resorts (The Boca Raton) to boutique retreats (A Sunset Chateau) and multi-unit groups (Minor Hotels, EVT, Mantra)—the underlying principles converge on empathy, continuous curiosity, and commercial discipline.")
    doc.append("- **Knowledge Base Utility:** This verbatim archive provides a rapid reference for hotel team training, leadership onboarding, and commercial strategy alignment.\n")

    q_out = os.path.join(QUESTIONS_DIR, f"{q['id']}.md")
    with open(q_out, 'w', encoding='utf-8') as f:
        f.write("\n".join(doc))

# Update Master README
readme_path = os.path.join(DERIVED_DIR, "README.md")
readme_content = f"""# The Hotelier Huddle: knowledge base architecture and index

> **An open-source knowledge engine built from all 20 verbatim transcripts of The Hotelier Huddle**  
> **Host and creator:** Shannon Knapp, CHIA (SKnapp Consulting)  
> **Audio editor and producer:** Heidi Egger  
> **Curator and knowledge engine architect:** Dr David Haberlah  
> **Total published episodes:** 20 episodes | **Local transcribed corpus:** 20 episodes (100% complete)

---

## Homage to the legacy of Shannon Knapp

This repository is an homage to the legacy of Shannon Knapp, CHIA. Until her last breath, Shannon was passionate about advancing the hotel profession alongside her best friends in the industry, the colleagues and leaders she interviewed across these 20 episodes.

Following her passing, her friends and collaborators brought this archive together so her work would endure: Heidi Egger engineered the audio and produced the recordings, and David Haberlah transcribed the corpus, built the open-source repository and hosts the Model Context Protocol server.

This archive preserves Shannon's contribution so her legacy continues to support future generations of hoteliers.

---

## Seven thematic virtual panels

The virtual panels synthesise verbatim dialogue across related episodes into thematic councils:

1. [Panel 01: Commercial and revenue management mastermind](virtual_panels/PANEL_01_Commercial_Alignment_Sales_vs_Revenue.md) (Purvey, Matthews, Camp, Godfrey, Borger)
   * *Core focus:* Shifting from vanity occupancy to net profitability (Net RevPAR, GOPPAR, TRevPAR); eliminating rate day-trading; applying MLOS demand filters; and managing channel distribution costs.
2. [Panel 02: AI operating system and intelligent hotel technology](virtual_panels/PANEL_02_AI_Technology_and_the_Human_Touch.md) (Purvey, Haberlah, Taylor, Xie, Buillet, Gempel)
   * *Core focus:* The AI operating system, enterprise data boundaries, SLMs vs. LLMs, RAG architecture, and preserving genuine human empathy alongside autonomous operational workflows.
3. [Panel 03: Crisis management and brand resilience](virtual_panels/PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience.md) (Purvey, Kalis, Weatherburn, Johnson, Buillet)
   * *Core focus:* Hurricane recovery, COVID resilience, brand reputation, and emergency leadership under disruption.
4. [Panel 04: Modern hotelier leadership and culture](virtual_panels/PANEL_04_Leadership_Culture_and_People_Over_Profit.md) (Kalis, Brady, Johnson, Wacher, Turner, Gempel)
   * *Core focus:* General manager leadership lessons; daily 15-minute leadership habits; prioritising employee culture (eNPS); frontline empowerment; and hiring leaders smarter than yourself.
5. [Panel 05: Non-linear careers and boardroom capabilities](virtual_panels/PANEL_05_Non_Linear_Careers_and_Boardroom_Skills.md) (D'Orazio, Johnson, Wacher, McBain, Fraser)
   * *Core focus:* Boardroom-grade skills, night audit to CEO, career pivots, and overcoming self-doubt in hospitality careers.
6. [Panel 06: Hotel development, precincts and asset strategy](virtual_panels/PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy.md) (Weatherburn, Taylor, Buillet, Turner)
   * *Core focus:* Masterplanning hotels: wellness as revenue, mixed-use precinct integration, adaptive reuse, strata-title economics, and owner-operator lifestyle balance.
7. [Panel 07: Frontline guest experience and service craft](virtual_panels/PANEL_07_Frontline_Guest_Experience_and_Service_Craft.md) (Kalis, Martin, Brady, D'Orazio, Xie)
   * *Core focus:* Frontline empathy, hyper-personalisation, concierge craft, service recovery, and turning high-friction guest moments into lifelong brand loyalty.

---

## Five signature question knowledge bases

Every question posed repeatedly by Shannon is indexed across all 20 transcripts:

1. [KB 01: The Accidental Hotelier (Origins and Career Entry)](question_knowledge_bases/KB_Q1_The_Accidental_Hotelier_Origins_and_Career_Pivots.md)
2. [KB 02: Will Sales and Revenue Ever See Eye to Eye?](question_knowledge_bases/KB_Q2_Will_Sales_and_Revenue_Ever_See_Eye_To_Eye.md)
3. [KB 03: Advice to Emerging Hoteliers and Younger Self](question_knowledge_bases/KB_Q3_Advice_to_Emerging_Hoteliers_and_Younger_Self.md)
4. [KB 04: Technology, AI and the Human Touch in Hospitality](question_knowledge_bases/KB_Q4_Technology_AI_vs_The_Human_Touch_in_Hospitality.md)
5. [KB 05: The Final Toast Anthology (Honouring Hospitality Workers)](question_knowledge_bases/KB_Q5_The_Final_Toast_Anthology_to_Hospitality_Workers.md)

---

## Provenance and source registers

For complete provenance, podcast metadata, and individual episode transcripts, refer to:
* [`../HOTELIER_HUDDLE_METADATA.json`](../HOTELIER_HUDDLE_METADATA.json)
* [`../HOTELIER_HUDDLE_PODCAST_METADATA.md`](../HOTELIER_HUDDLE_PODCAST_METADATA.md)
* [`../EPISODE_INVENTORY_GAP.md`](../EPISODE_INVENTORY_GAP.md)
* [`../PUBLICATION_READINESS_RECONCILIATION.md`](../PUBLICATION_READINESS_RECONCILIATION.md)
"""

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("Regenerated all 7 derived virtual panels, 5 question KBs, and master README.")
