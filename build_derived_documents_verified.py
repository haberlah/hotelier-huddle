import os
import json
import glob
import re

FOLDER = os.path.dirname(os.path.abspath(__file__))
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

PANEL_DEFS = [
    {
        'id': 'PANEL_01_Commercial_Alignment_Sales_vs_Revenue',
        'title': 'The Commercial and Revenue Management Mastermind: Net Profitability and Distribution',
        'theme': 'Shifting from vanity occupancy to net profitability (Net RevPAR, GOPPAR, TRevPAR); eliminating rate day-trading; applying MLOS demand filters; and managing channel distribution costs.',
        'panelists': [1, 3, 7, 17, 20],
        'turns_map': {
            1: [46, 47],
            3: [22, 23],
            7: [19, 20],
            17: [36, 37, 70, 71, 72],
            20: [67, 68, 75, 76]
        },
        'synthesis': [
            "Shifting from Vanity Occupancy to Net Profit: Full hotels are not necessarily the most profitable. High occupancy achieved through heavy OTA discounting inflates variable operating expenses and commission burdens, degrading net operating margins.",
            "Eliminating Rate Day-Trading: Top commercial leaders treat revenue management as strategic positioning rather than continuous tactical rate adjustments. Setting disciplined parameters and moving decisions into the 'done pile' creates mental clarity.",
            "De-Jargoning Commercial Communication: Revenue leaders must translate technical metrics (RevPAR, MPI, ARI) into plain business language so general managers, sales teams, and food and beverage directors understand commercial strategy.",
            "Collaborative Commercial Culture: Bridging the traditional divide between sales and revenue management requires shared profitability goals, mutual commercial empathy, and short, cross-departmental standups."
        ]
    },
    {
        'id': 'PANEL_02_AI_Technology_and_the_Human_Touch',
        'title': 'The AI Operating System and Intelligent Hotel Technology Council',
        'theme': 'The emerging AI operating system, enterprise data boundaries, SLMs vs LLMs, RAG architecture, and protecting genuine human empathy alongside autonomous operational workflows.',
        'panelists': [1, 5, 10, 11, 14, 18],
        'turns_map': {
            1: [114, 115],
            5: [33, 34, 40, 41],
            10: [113, 114],
            11: [43, 44],
            14: [22, 23],
            18: [61, 62, 63, 64]
        },
        'synthesis': [
            "Technology as an Operational Liberator: Automation and artificial intelligence should eliminate administrative friction and repetitive data entry, freeing staff to focus on genuine guest hospitality.",
            "Enterprise Data Boundaries and Trust: Deploying AI systems in hospitality demands strict isolation of proprietary commercial data and guest profiles from public model training datasets.",
            "The Irreplaceability of Human Empathy: While automated systems handle inquiries and booking changes efficiently, complex guest friction, emotional recovery, and hospitality magic depend entirely on human connection.",
            "Soft Skills as the Ultimate Edge: As analytical and predictive tasks become automated, emotional intelligence, persuasion, and cross-functional leadership become the primary differentiators for hospitality professionals."
        ]
    },
    {
        'id': 'PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience',
        'title': 'The Crisis Management and Brand Resilience Council',
        'theme': 'Navigating natural disasters, pandemics, PR crises, economic downturns, and market disruption with calm leadership and transparent brand communications.',
        'panelists': [1, 2, 8, 12, 14],
        'turns_map': {
            1: [19, 20],
            2: [23, 24],
            8: [66, 67],
            12: [50, 51, 52, 53],
            14: [6, 7]
        },
        'synthesis': [
            "Calm, Transparent Leadership in Crisis: Whether facing hurricane damage, sudden lockdown orders, or severe downturns, leadership requires clear, transparent communication with staff and guests.",
            "Industry Solidarity Over Pure Competition: During systemic crises like the COVID-19 pandemic, fierce commercial competitors must unite to advocate for industry survival, government wage support, and workforce retention.",
            "Brand Equity as Economic Insurance: Properties with distinctive, authentic brand identity weather downturns far better than commoditised assets, avoiding the destructive spiral of pure price discounting.",
            "Operational Adaptability: Surviving disruption requires rapid delegation, letting go of rigid procedural perfection, and empowering frontline operators to adapt to immediate physical realities."
        ]
    },
    {
        'id': 'PANEL_04_Leadership_Culture_and_People_Over_Profit',
        'title': 'The Modern Hotelier Leadership Council: People Over Spreadsheets and Frontline Empowerment',
        'theme': 'General Manager leadership lessons; daily 15-minute leadership habits; prioritising employee culture (eNPS); frontline empowerment; and hiring leaders smarter than yourself.',
        'panelists': [2, 6, 12, 13, 15, 18],
        'turns_map': {
            2: [45, 46, 47, 48],
            6: [28, 29, 30],
            12: [92, 93, 94, 95],
            13: [73, 74],
            15: [39, 40],
            18: [65, 66, 67, 68]
        },
        'synthesis': [
            "People Over Spreadsheets: Sustainable commercial results stem from supported, valued hotel teams. Prioritising employee net promoter scores (eNPS) directly correlates with guest satisfaction and property profitability.",
            "Daily Intentional Leadership Habits: Setting aside dedicated daily time to walk the floor, check in on frontline staff, and engage directly with teams builds trust faster than executive reports.",
            "Empowerment and Psychological Safety: Frontline staff must have clear authority to resolve guest grievances on the spot without fear of reprimand from management.",
            "Saying Yes to Growth: Fostering a culture where emerging professionals are encouraged to take on unfamiliar responsibilities accelerates career progression and drives organisational agility."
        ]
    },
    {
        'id': 'PANEL_05_Non_Linear_Careers_and_Boardroom_Skills',
        'title': 'The Non-Linear Career and Boardroom Capabilities Council',
        'theme': 'Recognising the high-level, boardroom-grade transferable skills of hotel professionals, navigating non-linear career pivots, and going from night audit to CEO.',
        'panelists': [9, 12, 13, 16, 19],
        'turns_map': {
            9: [37, 38],
            12: [16, 17],
            13: [41, 42],
            16: [66, 67],
            19: [92, 93]
        },
        'synthesis': [
            "Undervalued Hospitality Competencies: Hotel managers orchestrate complex, multi-million-dollar operational ecosystems daily. These management competencies directly transfer to corporate executive leadership, facilities, and board governance.",
            "The Night Audit Foundation: Starting in frontline, unsocial-hours roles builds thorough operational resilience, financial literacy, and crisis resolution skills that ground future executive leadership.",
            "Embracing Non-Linear Pivots: Hospitality careers rarely follow rigid straight lines. Diversifying across disciplines—from operations and sales to education and asset management—builds multifaceted perspective.",
            "Confidence and External Validation: Pursuing formal business education or professional board roles often validates what experienced hoteliers already practise intuitively on the hotel floor."
        ]
    },
    {
        'id': 'PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy',
        'title': 'The Hotel Development, Precincts and Asset Strategy Council',
        'theme': 'Masterplanning tomorrow’s hotels: wellness as revenue, mixed-use precinct integration, adaptive reuse, strata-title economics, and owner-operator lifestyle balance.',
        'panelists': [8, 10, 14, 15],
        'turns_map': {
            8: [35, 36, 37, 38],
            10: [71, 72],
            14: [6, 7],
            15: [49, 50]
        },
        'synthesis': [
            "Precinct Masterplanning and Mixed-Use Synergy: Modern hotel development thrives when integrated into vibrant, walkable commercial and cultural precincts rather than operating as isolated accommodation blocks.",
            "Wellness as an Integrated Revenue Engine: Transitioning wellness from an underutilised basement gym into a central guest amenity drives premium average daily rate (ADR) and guest length of stay.",
            "Strata-Title Realities: Managing strata-titled properties requires balancing relationships across dozens or hundreds of individual property owners alongside commercial guests, demanding specialised operational governance.",
            "Valuing the People in M&A: Acquiring hotel portfolios or management rights is fundamentally an acquisition of human capability and systems, not merely physical real estate."
        ]
    },
    {
        'id': 'PANEL_07_Frontline_Guest_Experience_and_Service_Craft',
        'title': 'The Frontline Guest Experience and Service Craft Council',
        'theme': 'Frontline empathy, hyper-personalisation, concierge craft, service recovery, and turning high-friction guest moments into lifelong brand loyalty.',
        'panelists': [2, 4, 6, 9, 11],
        'turns_map': {
            2: [9, 10],
            4: [86, 87],
            6: [58, 59],
            9: [23, 24],
            11: [51, 52, 53, 54]
        },
        'synthesis': [
            "Walking in the Guest's Shoes: Frontline staff must experience their property firsthand—dining in the restaurant, testing the amenities—to make authentic, confident recommendations.",
            "Service Recovery Philosophy: When guest friction occurs, arguing over minor charges (such as minibar disputes) destroys brand goodwill. Immaterial disputes should be conceded gracefully to preserve relationships.",
            "Agility Over Rigid Scripting: High-touch hospitality requires staff to adapt to unexpected situations and weather sudden operational disruptions with calm poise.",
            "The Power of Frontline Curiosity: Demonstrating genuine curiosity about guest preferences and listening actively creates moments of hyper-personalisation that generic automation cannot replicate."
        ]
    }
]

for p in PANEL_DEFS:
    doc = []
    doc.append(f"# {p['title']}\n")
    doc.append(f"**Thematic Focus:** {p['theme']}  ")
    doc.append(f"**Moderator:** Shannon Knapp, CHIA (Founder, SKnapp Consulting)  ")
    doc.append(f"**Corpus Coverage:** Selected thematic panel from verified verbatim corpus  \n")
    doc.append("---\n")
    doc.append("## Virtual Panel Participants\n")
    
    for ep_num in p['panelists']:
        ep_info = EP_META.get(ep_num)
        if ep_info:
            g = ep_info['guest']
            src_url = g['sources'][0]['source_url'] if g.get('sources') else "https://podcasters.spotify.com/pod/show/hotelier-huddle"
            doc.append(f"* **{g['name']}** — {g['title']}, *{g['organization']}* (Episode {ep_num:02d}: *{ep_info['published_title']}*, Published {ep_info['published_date_utc'][:10]})")
            doc.append(f"  *Source Provenance:* [{src_url}]({src_url})\n")
            
    doc.append("---\n")
    doc.append("## Verbatim Panel Discussions and Dialogue Exchanges\n")
    
    for ep_num in p['panelists']:
        ep_info = EP_META.get(ep_num)
        turns = ALL_TRANSCRIPTS[ep_num]['turns']
        turn_indices = p['turns_map'].get(ep_num, [])
        if ep_info and turn_indices:
            doc.append(f"### Expert Perspective: {ep_info['guest']['name']} (Episode {ep_num:02d})\n")
            for idx in turn_indices:
                t = turns[idx]
                doc.append(f"{t['timestamp']} **{t['speaker']}:** {t['text']}\n")
            doc.append("")
            
    doc.append("---\n")
    doc.append("## Key Synthesis and Actionable Takeaways\n")
    for s in p['synthesis']:
        doc.append(f"- **{s.split(':')[0]}:** {':'.join(s.split(':')[1:]).strip()}")
    doc.append("")
    
    p_out = os.path.join(PANELS_DIR, f"{p['id']}.md")
    with open(p_out, 'w', encoding='utf-8') as f:
        f.write("\n".join(doc))

QB_DEFS = [
    {
        'id': 'KB_Q1_The_Accidental_Hotelier_Origins_and_Career_Pivots',
        'title': 'The Accidental Hotelier: Origins, Unexpected Entrees and Career Pivots',
        'shannon_core_question': 'How did you get your start in hospitality, and was it a deliberate career choice or an accidental journey?',
        'context': "Throughout The Hotelier Huddle, host Shannon Knapp uncovers the diverse and often accidental journeys that lead talented professionals into the hotel industry. Across 20 episodes, industry leaders share how backgrounds spanning law, teaching, market research, geology, information systems, youth work, and frontline night audit evolved into distinguished hospitality careers.",
        'turns_map': {
            1: [3, 4, 7, 8],
            2: [3, 4],
            3: [176, 177],
            4: [2, 3, 4, 5],
            5: [7, 8],
            6: [33, 34, 35],
            7: [4, 5, 6],
            8: [11, 12, 13],
            9: [7, 8, 9],
            10: [7, 8],
            11: [9, 10, 11],
            12: [16, 17],
            13: [41, 42],
            14: [22, 23],
            15: [3, 4],
            16: [27, 28],
            17: [6, 7, 8],
            18: [15, 16],
            19: [8, 9],
            20: [43, 44, 45]
        },
        'takeaways': [
            "The Power of Non-Linear Backgrounds: Most senior leaders did not begin with a narrow hotel management degree; their breadth across teaching, law, IT, and sciences enriches their commercial and operational judgment.",
            "Frontline Empathy as a Career Foundation: Leaders who began in night audit, restaurant service, or reservations retain deep respect for operational staff, making them more empathetic and effective executives.",
            "Embracing Serendipity: Stepping through unexpected career doors often leads to lifelong professional passions."
        ]
    },
    {
        'id': 'KB_Q2_Will_Sales_and_Revenue_Ever_See_Eye_To_Eye',
        'title': 'The Commercial Divide: Will Sales and Revenue Ever See Eye to Eye?',
        'shannon_core_question': 'Why is there such persistent tension between Sales and Revenue Management, and how do we align them around shared profitability?',
        'context': "One of the most enduring debates in hotel management is the structural tension between Sales (incentivised by room night volume and relationships) and Revenue Management (incentivised by rate integrity, yield, and profit). In these curated exchanges, commercial directors and consultants unpack how to dissolve this tension and align around net profitability.",
        'turns_map': {
            1: [46, 47],
            3: [159, 160, 163, 164],
            4: [76, 77, 78, 79],
            7: [19, 20],
            11: [37, 38],
            13: [36, 37, 38, 39],
            17: [36, 37, 70, 71, 72],
            18: [61, 62, 63, 64],
            20: [67, 68, 75, 76]
        },
        'takeaways': [
            "Shared Commercial Metrics: Aligning sales incentives with net revenue and GOPPAR rather than gross top-line volume immediately harmonises priorities.",
            "Speaking Plain English: Revenue managers must drop technical acronyms and explain the business rationale behind pricing decisions.",
            "Mutual Discipline: Sales teams should consult revenue managers early before quoting discounted group rates, while revenue managers must recognise the commercial value of long-term corporate relationships."
        ]
    },
    {
        'id': 'KB_Q3_Advice_to_Emerging_Hoteliers_and_Younger_Self',
        'title': 'Wisdom to Emerging Hoteliers and Advice to Your Younger Self',
        'shannon_core_question': 'What advice would you give to a young professional starting out in hospitality today, or to your younger self early in your career?',
        'context': "In this signature inquiry, Shannon invites leaders to reflect on what really matters over a 20-to-30-year career. The resulting counsel covers managing stress, building boardroom credibility, developing patience, and embracing curiosity across hotel departments.",
        'turns_map': {
            1: [138, 139, 142],
            2: [45, 46, 47, 48],
            3: [22, 23],
            4: [86, 87, 94, 95],
            5: [127, 128],
            6: [68, 69, 70, 71],
            7: [65, 66, 67, 68],
            8: [82, 83],
            9: [23, 24],
            10: [149, 150, 151, 152],
            11: [51, 52, 53, 54],
            12: [92, 93, 94, 95],
            13: [91, 92, 93, 94],
            14: [6, 7],
            15: [39, 40],
            16: [66, 67],
            17: [69, 70, 71, 72],
            18: [65, 66, 67, 68],
            19: [92, 93, 108, 109],
            20: [109, 110, 115, 116]
        },
        'takeaways': [
            "Earning Boardroom Credibility: Master your existing discipline before telling others how to do their jobs. True influence comes from demonstrated competence.",
            "Patience and Delegation: Recognize that 90% execution by an empowered team is far better than burning out trying to achieve 100% solo perfection.",
            "Owning Your Value: Hotel management skills are world-class leadership capabilities. Hoteliers should carry genuine pride in their versatility and operational craft.",
            "Perspective and Resilience: Don't take short-term friction too seriously. In the words of Francis Purvey's mantra: 'Always look on the bright side of life.'"
        ]
    },
    {
        'id': 'KB_Q4_Technology_AI_vs_The_Human_Touch_in_Hospitality',
        'title': 'Technology, AI and the Human Touch: Threat or Support?',
        'shannon_core_question': 'Do you see emerging technology and AI as a threat or a support to hotel operations, and how do we protect genuine human connection?',
        'context': "As autonomous workflows, chatbots, and AI revenue algorithms enter the hospitality ecosystem, Shannon and her guests examine the critical boundary between technological efficiency and human connection. Across these dialogues, technology leaders and hoteliers outline how to augment staff without eroding the hospitality spirit.",
        'turns_map': {
            1: [114, 115],
            2: [3, 4],
            3: [8, 9, 10, 11],
            5: [33, 34, 40, 41],
            9: [23, 24],
            10: [113, 114],
            11: [43, 44],
            14: [22, 23],
            18: [61, 62]
        },
        'takeaways': [
            "AI Automates Administrative Burden: Software should eliminate rote calculations, data extraction, and repetitive guest queries.",
            "Protecting Guest Empathy: The emotional core of hospitality—welcoming a weary traveller, de-escalating frustration, tailoring a personal stay—cannot be replicated by algorithms.",
            "Enterprise Data Sovereignty: Hotel operators must ensure enterprise data integrity when integrating external models with core property systems."
        ]
    },
    {
        'id': 'KB_Q5_The_Final_Toast_Anthology_to_Hospitality_Workers',
        'title': 'The Final Toast Anthology: Honoring Hospitality Workers Worldwide',
        'shannon_core_question': 'If you are raising a glass to celebrate hospitality workers everywhere, what would your toast be?',
        'context': "At the close of each episode of The Hotelier Huddle, host Shannon Knapp invited her guest to raise a glass and deliver a final toast to hospitality workers worldwide. These 20 verbatim toasts serve as an inspiring tribute to the resilience, generosity, and camaraderie of the global hotel community.",
        'turns_map': {
            1: [148, 149],
            2: [51, 52],
            3: [191, 192],
            4: [126, 127],
            5: [131, 132, 133, 134],
            6: [154, 155],
            7: [73, 74],
            8: [96, 97],
            9: [103, 104],
            10: [167, 168],
            11: [57, 58],
            12: [162, 163],
            13: [95, 96],
            14: [65, 66],
            15: [59, 60],
            16: [108, 109],
            17: [85, 86],
            18: [101, 102],
            19: [110, 111],
            20: [109, 110]
        },
        'takeaways': [
            "A Heartfelt Tribute: A universal celebration of frontline housekeepers, night auditors, receptionists, chefs, and managers who craft unforgettable guest memories every day.",
            "Community and Resilience: Reflecting the deep, unbreakable camaraderie that connects hospitality workers across borders and generations."
        ]
    }
]

for q in QB_DEFS:
    doc = []
    doc.append(f"# Knowledge Base: {q['title']}\n")
    doc.append(f"**Shannon's Core Inquiry:** *\"{q['shannon_core_question']}\"*  ")
    doc.append(f"**Host and Creator:** Shannon Knapp, CHIA (SKnapp Consulting)  ")
    doc.append(f"**Corpus Coverage:** {len(q['turns_map'])} verified episode dialogues from complete verbatim corpus  \n")
    doc.append("---\n")
    doc.append("## Strategic Context and Significance\n")
    doc.append(f"{q['context']}\n")
    doc.append("---\n")
    doc.append("## Verbatim Responses from the Expert Panel\n")
    
    for ep_num in sorted(q['turns_map'].keys()):
        ep_info = EP_META.get(ep_num)
        turns = ALL_TRANSCRIPTS[ep_num]['turns']
        turn_indices = q['turns_map'][ep_num]
        
        g_name = ep_info['guest']['name']
        g_title = ep_info['guest']['title']
        g_org = ep_info['guest']['organization']
        src_url = ep_info['guest']['sources'][0]['source_url'] if ep_info['guest'].get('sources') else "https://podcasters.spotify.com/pod/show/hotelier-huddle"
        
        doc.append(f"### Episode {ep_num:02d}: {g_name} ({g_org})\n")
        doc.append(f"**Guest:** {g_name} — *{g_title}, {g_org}*  ")
        doc.append(f"**Episode:** *{ep_info['published_title']}* ({ep_info['published_date_utc'][:10]})  ")
        doc.append(f"**Source Provenance:** [{src_url}]({src_url})\n")
        
        for idx in turn_indices:
            t = turns[idx]
            doc.append(f"{t['timestamp']} **{t['speaker']}:** {t['text']}\n")
        doc.append("")
        
    doc.append("---\n")
    doc.append("## Comparative Analysis and Key Insights\n")
    for t_item in q['takeaways']:
        doc.append(f"- **{t_item.split(':')[0]}:** {':'.join(t_item.split(':')[1:]).strip()}")
    doc.append("")
    
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

Every core inquiry posed by Shannon is indexed across the verified corpus:

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

# Verbatim Fidelity Audit
print("\n--- Running Master Verbatim Fidelity & Integrity Audit ---")
all_derived_files = glob.glob(os.path.join(PANELS_DIR, "*.md")) + glob.glob(os.path.join(QUESTIONS_DIR, "*.md"))
total_quotes_checked = 0
matches = 0

for df in sorted(all_derived_files):
    with open(df, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all speaker turns
    turn_matches = re.findall(r'(\[\d{1,2}:\d{2}(?::\d{2})?\])\s*\*\*([^*]+?):\*\*\s*(.*)', content)
    for ts, spk, text in turn_matches:
        total_quotes_checked += 1
        found = False
        text_clean = text.strip()
        for ep_num, ep_data in ALL_TRANSCRIPTS.items():
            for t in ep_data['turns']:
                if t['timestamp'] == ts and t['speaker'] == spk and t['text'] == text_clean:
                    found = True
                    break
            if found:
                break
        if found:
            matches += 1
        else:
            print(f"MISMATCH in {os.path.basename(df)}: {ts} {spk}: {text_clean[:60]}...")

fidelity = (matches / total_quotes_checked * 100) if total_quotes_checked > 0 else 0
print(f"Audit Complete: {matches}/{total_quotes_checked} ({fidelity:.1f}%) quotes matched character-for-character.")
assert matches == total_quotes_checked, f"Fidelity error: {total_quotes_checked - matches} quotes failed to match!"
print("Regenerated all 7 derived virtual panels, 5 question KBs, and master README with 100.0% verbatim fidelity.")
