# The Hotelier Huddle — Open Source AI Knowledge Base

[![License: CC BY 4.0](https://img.shields.io/badge/Content_License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/Code_License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Corpus Status](https://img.shields.io/badge/Episodes-20%2F20_Complete-success.svg)](#episode-catalog)
[![Audio Hours](https://img.shields.io/badge/Audio-12.6_Hours-purple.svg)](#corpus-metrics)
[![Verbatim Fidelity](https://img.shields.io/badge/Quote_Fidelity-100.0%25_(340%2F340)-gold.svg)](#derived-knowledge-base)

> **A comprehensive, AI-native archive of *The Hotelier Huddle* podcast transcripts, multi-dimensional virtual panels, and hospitality terminology registers, formatted with YAML frontmatter for seamless ingestion by Claude Code, Cursor, and Model Context Protocol (MCP) clients.**

* **Host & Creator:** **Shannon Knapp, CHIA** (Founder & Principal, SKnapp Consulting)  
* **Audio Editor & Producer:** **Heidi Egger**  
* **Curator & Knowledge Engine Architect:** **Dr. David Haberlah**  
* **Published RSS Feed:** [anchor.fm/s/109667b00/podcast/rss](https://anchor.fm/s/109667b00/podcast/rss)  
* **Apple Podcasts:** [id1840076396](https://podcasts.apple.com/us/podcast/hotelier-huddle/id1840076396)  
* **Spotify for Podcasters:** [podcasters.spotify.com/pod/show/hotelier-huddle](https://podcasters.spotify.com/pod/show/hotelier-huddle)  

---

## 🕊️ In Memory of Shannon Knapp, CHIA

*The Hotelier Huddle* was Shannon Knapp's homage to the hotel industry and the global community of hoteliers who meant the world to her. Spanning 26+ years of commercial, reservations, and revenue optimization expertise across the Asia-Pacific region, Shannon brought unmatched warmth, intellectual rigor, and humor to these conversations. This open-source knowledge repository preserves her legacy, making the hard-won wisdom of these 20 hospitality leaders accessible for research, team training, and AI exploration.

---

## 🚀 Quick Start for AI Tools & MCP

### 1. Using with Claude Code / Cursor
Clone or point your AI assistant directly at this directory:
```bash
git clone https://github.com/haberlah/hotelier-huddle.git
```
All transcripts in `transcripts/` feature standardized YAML frontmatter, strict monotonic timestamps, and verified speaker diarization. You can ask:
* *"According to Tamie Matthews and Matt Camp, why does rate day-trading destroy hotel profitability?"*
* *"What are Dr. David Haberlah's frameworks for enterprise data boundaries and AI Operating Systems in hotels?"*
* *"Synthesize Greg Brady's 8 leadership lessons for a newly promoted General Manager."*

### 2. Using with Model Context Protocol (MCP)
Run the bundled MCP server locally with zero installation using `uvx`:
```bash
uvx --from ./mcp_server hotelier-huddle-mcp
```
Or add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "hotelier-huddle": {
      "command": "python3",
      "args": ["/path/to/hotelier-huddle/mcp_server/server.py"]
    }
  }
}
```

---

## 📂 Repository Layout

```text
hotelier-huddle/
├── README.md                      # Project overview, quick start, and architecture
├── LICENSE.md                     # Open source license (Code: MIT; Content: CC BY 4.0)
├── CONTRIBUTING.md                # Contribution guidelines and transcript standardisation rules
├── .gitignore                     # Git rules (audio binaries excluded from repo)
├── index.json                     # Lightweight master index for instant MCP / RAG consumption
├── HOTELIER_HUDDLE_METADATA.json  # Canonical deep provenance & metadata register
├── HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md  # Standardized industry glossary
├── HOTELIER_HUDDLE_EXPERT_PANEL_MATRIX.md               # 7 Thematic virtual panels matrix
├── PUBLICATION_READINESS_RECONCILIATION.md              # Master verification & audit report
│
├── transcripts/                   # 20 Verbatim transcripts with YAML frontmatter
│   ├── 01-Will Sales and Revenue Ever See Eye To Eye-Francis Purvey.md
│   └── ...
│
├── derived_knowledge_base/        # Multi-dimensional thematic synthesis
│   ├── README.md                  # Knowledge base index and guide
│   ├── virtual_panels/            # 7 Thematic cross-episode roundtable councils
│   └── question_knowledge_bases/  # 5 Signature cross-corpus question repositories
│
├── mcp_server/                    # Model Context Protocol (MCP) server implementation
│   ├── server.py                  # FastMCP Python server (search, resources, tools)
│   └── pyproject.toml             # uv package specification
│
└── audio/                         # Raw .m4a audio files (downloadable via script)
```

---

## 📋 Episode Catalog & Holdings (All 20 Episodes)

| Ep # | Published Episode Title | Published Date | Runtime | Word Count | Featured Guest & Organization | Controlled Tags |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **01** | Will Sales and Revenue Ever See Eye To Eye? | 2025-09-16 | 53:51 | 8,790 | **Francis Purvey** (*Sunlark Associates*) | `sales`, `revenue-management`, `trevpar` |
| **02** | Fake It Until You Become It | 2025-09-16 | 32:04 | 5,466 | **Alexia Kalis** (*Kalis Hospitality Group*) | `leadership`, `fb-strategy`, `pricing` |
| **03** | Are Full Hotels Always The Most Profitable? | 2025-10-02 | 39:21 | 6,674 | **Tamie Matthews** (*RevenYou*) | `net-revpar`, `goppar`, `otas`, `content-parity` |
| **04** | The Accidental Hotelier: Tracy Martin on Sales | 2025-10-09 | 40:22 | 6,568 | **Tracy Martin** (*The Wisdom Well*) | `hotel-sales`, `solo-consulting`, `service-craft` |
| **05** | The AI Operating System is Coming: Are Hotels Ready? | 2025-10-17 | 54:45 | 10,300 | **Dr. David Haberlah** (*Hotel Tech*) | `ai`, `hotel-tech`, `data-security`, `pms` |
| **06** | 8 Leadership Lessons from Award Winning Hotel GM | 2025-10-22 | 24:26 | 4,256 | **Greg Brady** (*Sofitel Sydney / Accor*) | `general-management`, `leadership`, `empowerment` |
| **07** | Are You Revenue Managing or Day Trading? | 2025-10-29 | 31:04 | 5,731 | **Matt Camp** (*Independent Consultant*) | `day-trading`, `anecdata`, `distribution` |
| **08** | Crafting a Distinct Brand: Lessons from an Expert | 2025-11-07 | 40:29 | 7,295 | **Eve Weatherburn** (*Brand Journey Partner*) | `hotel-branding`, `luxury-positioning`, `resilience` |
| **09** | 5-Star Guest Relations Agent on Profit & Purpose | 2025-11-14 | 38:46 | 6,223 | **Joaquin D'Orazio** (*The Boca Raton*) | `guest-relations`, `hyper-personalisation`, `service` |
| **10** | Precincts, Wellness & What Every Hotelier Should Know | 2025-11-18 | 45:45 | 7,560 | **Andrew Taylor** (*Cre8tive Hotels*) | `development`, `precincts`, `wellness-revenue` |
| **11** | Rising Through Reservations: Business Mindset & AI | 2025-12-04 | 28:18 | 4,593 | **Jasmine Xie** (*PARKROYAL Parramatta*) | `reservations`, `waitlists`, `distribution` |
| **12** | Night Audit to CEO: Saying Yes Changes Everything | 2025-12-12 | 47:12 | 8,550 | **Michael Johnson** (*Accommodation Australia*) | `night-audit-to-ceo`, `boardroom-skills`, `relove` |
| **13** | Hotel Sales Consultant: The Magic is in You | 2025-12-21 | 31:15 | 5,179 | **Kelley Wacher** (*Corporate Magic™*) | `sales-consulting`, `executive-coaching`, `mindset` |
| **14** | Hotel Owner Insights: 23 Years Of Building Balance | 2026-01-07 | 25:51 | 4,588 | **Jean-Christophe Buillet** (*A Sunset Chateau*) | `owner-operator`, `boutique-luxury`, `sedona` |
| **15** | How I Grew 48 Hotels Worth $1.8 Billion | 2026-01-21 | 36:19 | 7,110 | **Andrew Turner** (*Minor Hotels*) | `development`, `strata-title`, `scaling` |
| **16** | You're a Rock Star (Someone Had to Tell You) | 2026-02-19 | 32:45 | 5,119 | **Janet McBain** (*Facilities Management*) | `facilities`, `transferable-skills`, `boardroom` |
| **17** | What Rental Cars Taught Me About Selling Rooms | 2026-02-27 | 33:36 | 5,482 | **Mike Godfrey** (*Commercial Strategist*) | `revenue-management`, `car-rental`, `mlos`, `pacing` |
| **18** | Two Habits That Will Change How You Lead | 2026-04-19 | 32:47 | 5,495 | **Heidi Gempel** (*HGE International*) | `leadership-habits`, `emotional-intelligence` |
| **19** | How to Navigate Career Changes | 2026-06-21 | 42:51 | 7,682 | **Stephen Fraser** (*EVT Connect Hospitality*) | `career-pivots`, `contact-centers`, `modernization` |
| **20** | Hotel Sales Skills that Fill Planes | 2026-07-11 | 45:25 | 8,577 | **Matthew Borger** (*Newcastle Airport / DPS*) | `hotel-sales`, `aviation`, `destination-marketing` |

---

## 🏛️ The 7 Thematic Virtual Panels

The derived knowledge base synthesizes verbatim dialogue across related episodes into thematic roundtable councils:

1. 📊 [**Panel 01: Commercial & Revenue Management Mastermind**](derived_knowledge_base/virtual_panels/PANEL_01_Commercial_Alignment_Sales_vs_Revenue.md) — *Purvey, Matthews, Camp, Godfrey, Borger*
2. 🤖 [**Panel 02: AI Operating System & Intelligent Hotel Tech**](derived_knowledge_base/virtual_panels/PANEL_02_AI_Technology_and_the_Human_Touch.md) — *Haberlah, Xie, Taylor, Buillet, Gempel, Purvey*
3. 🛡️ [**Panel 03: Crisis Management & Brand Resilience**](derived_knowledge_base/virtual_panels/PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience.md) — *Purvey, Kalis, Weatherburn, Johnson, Buillet*
4. 👥 [**Panel 04: Modern Hotelier Leadership & Culture**](derived_knowledge_base/virtual_panels/PANEL_04_Leadership_Culture_and_People_Over_Profit.md) — *Brady, Kalis, Johnson, Wacher, Turner, Gempel*
5. 🚀 [**Panel 05: Non-Linear Careers & Boardroom Capabilities**](derived_knowledge_base/virtual_panels/PANEL_05_Non_Linear_Careers_and_Boardroom_Skills.md) — *D'Orazio, Johnson, Wacher, McBain, Fraser*
6. 🏗️ [**Panel 06: Hotel Development, Precincts & Asset Strategy**](derived_knowledge_base/virtual_panels/PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy.md) — *Weatherburn, Taylor, Buillet, Turner*
7. 🛎️ [**Panel 07: Frontline Guest Experience & Service Craft**](derived_knowledge_base/virtual_panels/PANEL_07_Frontline_Guest_Experience_and_Service_Craft.md) — *Kalis, Martin, Brady, D'Orazio, Xie*

---

## 📊 Corpus Metrics & Verbatim Verification

* **Total Audio Runtime:** **12 hours, 37 minutes, 21 seconds**
* **Total Words Transcribed:** **131,238 words**
* **Total Speaker Turns:** **2,406 turns**
* **Verbatim Quote Verification:** **340 of 340 (100.0%)** quoted turns in `derived_knowledge_base/` match source transcripts character-for-character.
* **Timestamp Monotonicity:** **100% strictly monotonic** (0 regressions across 2,400+ turns).
