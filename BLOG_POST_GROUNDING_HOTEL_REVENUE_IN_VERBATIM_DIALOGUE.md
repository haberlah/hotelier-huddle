# Shannon Knapp's final masterclass: Preserving The Hotelier Huddle as an interactive AI knowledge base

**David Haberlah**  
*Published 6 September 2026*

---

Hospitality revenue management is both a science and a craft. Advanced software can generate demand forecasts and rate hurdles, but thriving hotels still require human judgement and experience. Balancing occupancy against profit, controlling distribution costs, and aligning sales with revenue and brand must be learned on the hotel floor.

In September 2025, veteran industry consultant Shannon Knapp, CHIA (known to colleagues as *It's a Sknapp*), launched *The Hotelier Huddle* podcast with producer and editor Heidi Egger to capture that craft from experienced leaders, broadcasting across [Spotify](https://open.spotify.com/show/5P55u6SOBiyu0zX0knm4U5), [Apple Podcasts](https://podcasts.apple.com/au/podcast/hotelier-huddle/id1840076396), and [YouTube](https://www.youtube.com/@HotelierHuddle). At [SiteMinder](https://www.siteminder.com), Shannon, Heidi, and I worked together on Dynamic Revenue Plus, building predictive tools for accommodation providers ([SiteMinder, 2024](https://www.siteminder.com)). When Shannon later invited me onto [Episode 05](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/The-AI-Operating-System-is-Coming-Are-Hotels-Ready-e39l8k9) to discuss AI in hospitality ([Knapp, 2025](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/The-AI-Operating-System-is-Coming-Are-Hotels-Ready-e39l8k9)), we returned to that same premise: even the best algorithms cannot replace a broader commercial perspective. Without that grounding, less experienced hoteliers and revenue managers can fall into tactical traps, such as adjusting prices hourly against competitor screens—which Matt Camp characterised in [Episode 07](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Are-you-Revenue-Managing-or-Day-Trading-e389fm1) as commercial "day-trading" ([Knapp, 2026](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Are-you-Revenue-Managing-or-Day-Trading-e389fm1)).

Shannon often said that her goal was to produce at least 21 episodes. That milestone places a show in the top 1% of all podcasts ever produced ([Goldstein, 2021](https://amplifimedia.com)). Her sudden passing earlier this year left the hospitality community in deep shock and sadness, prompting moving tributes from industry colleagues across the [Hospitality Sales and Marketing Association International (HSMAI Asia Pacific)](https://asia.hsmai.org/team/shannon-knapp/)—including a heartfelt [memorial tribute](https://asia.hsmai.org/wp-content/uploads/sites/12/2018/09/shannon-memorial-jackie.mp4) by HSMAI President Jackie Douglas. Episode 20 remained Shannon's final recorded conversation, released posthumously. To honour her 21-episode milestone and preserve the executive wisdom she brought together, Heidi and I developed a 21st edition ([Haberlah & Egger, 2026](https://github.com/haberlah/hotelier-huddle)). Rather than another audio recording, we turned the podcast into an accessible knowledge base. We adopted the open-knowledge repository model used in technology by Lenny Rachitsky ([*Lenny's Podcast*](https://www.lennyspodcast.com); [Rachitsky, 2024](https://www.lennyspodcast.com)). We transcribed, diarised, and audited all 888 minutes of dialogue, built a canonical 42-term hospitality terminology register, and deployed a Model Context Protocol (MCP) server that allows hoteliers and AI agents to query 20 industry leaders. This post outlines the corpus structure, the technical implementation connecting language models to verified dialogue, and how to access it.

---

## The podcast knowledge base corpus

Transforming 14.8 hours of conversational audio into an AI-addressable knowledge base required structured data engineering and strict editorial curation. Speech-to-text diarisation alone leaves conversational drift, property-specific shorthand, and fragmented arguments that degrade semantic search. 

To create a dependable reference, we structured the repository into four functional tiers:

```
hotelier-huddle/
├── transcripts/                                   # 20 audited verbatim transcripts
│   ├── 01-will-sales-and-revenue-ever-see-eye-to-eye.md
│   └── ... [20 complete markdown transcripts]
├── derived_knowledge_base/
│   ├── virtual_panels/                            # 7 thematic multi-turn roundtables
│   │   ├── PANEL_01_Commercial_Alignment_Sales_vs_Revenue.md
│   │   └── ... [PANEL_02 through PANEL_07]
│   └── question_knowledge_bases/                  # 5 signature question repositories
│       ├── KB_Q1_The_Accidental_Hotelier_Origins_and_Career_Pivots.md
│       └── ... [KB_Q2 through KB_Q5]
├── mcp_server/                                    # Python FastMCP server implementation
├── cloudflare_worker/                             # Cloudflare Edge Worker deployment bundle
├── HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md
├── HOTELIER_HUDDLE_METADATA.json
├── LICENSE                                        # CC BY-NC-SA 4.0 (Knowledge) & MIT (Code)
└── SECURITY.md                                    # Responsible disclosure policy
```

### Quantitative inventory

The dataset reflects the following audited metrics:
* **Episodes published:** 20 complete episodes.
* **Recording window:** 16 September 2025 to 11 July 2026.
* **Total runtime:** 14 hours, 48 minutes, 22 seconds of spoken dialogue.
* **Transcribed volume:** 234,180 words across 1,842 discrete speaker turns.
* **Thematic Virtual Panels:** 7 multi-turn roundtables synthesising debate across core operational domains.
* **Signature Question Knowledge Bases:** 5 cross-corpus repositories indexing recurring inquiries across all 20 episodes.
* **Audited verbatim citations:** 458 character-for-character quotes validated against audio timestamps.

### Industry contributors across 8 operational disciplines

Shannon Knapp convened 20 leaders representing General Managers, Revenue Directors, Sales Leaders, Technology Founders, Consultants, Asset Directors, Tourism Chairs, and Frontline Concierges:

* **Episode 01: Francis Purvey** (Sales Leader · Executive Vice President, Sunlark Associates) — [Will Sales and Revenue Ever See Eye to Eye?](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Will-Sales-and-Revenue-Ever-See-Eye-To-Eye-e389aht)
* **Episode 02: Alexia Kalis** (General Manager & Executive Leader · Chief Executive Officer, Kalis Hospitality Group) — [Fake It Until You Become It: Crisis Leadership, Culture & Heritage](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Fake-It-Until-You-Become-It-e389fm3)
* **Episode 03: Tamie Matthews** (Revenue Director · Founder & Principal Consultant, RevenYou) — [Are Full Hotels Always the Most Profitable? Net RevPAR vs Vanity Occupancy](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Are-Full-Hotels-Always-The-Most-Profitable-e39038n)
* **Episode 04: Tracy Martin** (Sales Leader · Founder & Commercial Consultant, The Wisdom Well) — [The Accidental Hotelier: Sales, Solo Ventures, and Staying Power](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/The-Accidental-Hotelier-Tracy-Martin-on-Sales--Solo-Ventures--and-Staying-Power-e399s5a)
* **Episode 05: Dr David Haberlah** (Technology Leader · AI Globalisation Leader, SiteMinder) — [The AI Operating System is Coming: Are Hotels Ready?](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/The-AI-Operating-System-is-Coming-Are-Hotels-Ready-e39l8k9)
* **Episode 06: Greg Brady** (General Manager · Former General Manager, Sofitel Sydney Darling Harbour) — [8 Leadership Lessons from an Award-Winning Hotel General Manager](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/8-Leadership-Lessons-from-an-Award-Winning-Hotel-General-Manager-e39saeu)
* **Episode 07: Matt Camp** (Revenue Director · Revenue & Distribution Manager, Independent Consultant) — [Are You Revenue Managing or Day Trading?](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Are-You-Revenue-Managing-or-Day-Trading--With-Matt-Camp-e3a6ijj)
* **Episode 08: Eve Weatherburn** (Consultant & Brand Strategist · Founder & Managing Director, Brand Journey Partner) — [Crafting a Distinct Brand: Lessons from a Hotel Industry Expert](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Crafting-a-Distinct-Brand-Lessons-from-a-Hotel-Industry-Expert-e3akh6j)
* **Episode 09: Joaquin D’Orazio** (Frontline Concierge · Guest Relations Agent & Concierge, The Boca Raton) — [A Five Star Hotel Guest Relations Agent on Blending Profit, Purpose & Hyper-Personalisation](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/A-Five-Star-Hotel-Guest-Relations-Agent-on-Blending-Profit--Purpose--Hyper-Personalisation-e3aum20)
* **Episode 10: Andrew Taylor** (Asset Director & Strategic Advisor · Founder & Strategic Advisor, Cre8tive Hotels & Lifestyle) — [Precincts, Wellness & What Every Hotelier Should Know About Tomorrow’s Hotels](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Precincts--Wellness--What-Every-Hotelier-Should-Know-About-Tomorrows-Hotels-e3b4l0m)
* **Episode 11: Jasmine Xie** (Frontline Leader & Reservations Director · Reservations & Distribution Leader, PARKROYAL Parramatta) — [Rising Through Reservations: The Business Mindset, AI’s Limits, and Why Waitlists Matter](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Rising-Through-Reservations-The-Business-Mindset--AIs-Limits--and-Why-Waitlists-Matter-e3bs347)
* **Episode 12: Michael Johnson** (General Manager & Executive Leader · Former CEO, Accommodation Australia) — [Night Audit to CEO: Saying Yes Changes Everything](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Night-Audit-to-CEO-Saying-Yes-Changes-Everything-e3c8laf)
* **Episode 13: Kelley Wacher** (Sales Leader & Executive Coach · Founder & Executive Coach, Corporate Magic™) — [Hotel Sales Consultant: The Magic is in You](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Hotel-Sales-Consultant-The-Magic-is-in-You-e3ckvjg)
* **Episode 14: Jean-Christophe Buillet** (Asset Director & Owner-Operator · Owner-Operator, A Sunset Chateau, Sedona) — [Hotel Owner Insights: 23 Years Of Building Balance](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Hotel-Owner-Insights-23-Years-Of-Building-Balance-e3d9tvr)
* **Episode 15: Andrew Turner** (Asset Director & Development Leader · Head of Development — Australia, Minor Hotels) — [How I Grew 48 Hotels Worth $1.8 Billion: Career Advice for Hoteliers](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/How-I-Grew-48-Hotels-Worth-1-8-Billion-Career-Advice-for-Hoteliers-with-Andrew-Turner-e3dtt6o)
* **Episode 16: Janet McBain** (General Manager & Facilities Executive · Facilities Management Executive & Former Hotel GM) — [You’re a Rock Star (Someone Had to Tell You): Operational Resilience & Facilities](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Youre-a-Rock-Star-Someone-Had-to-Tell-You-e3f9sji)
* **Episode 17: Mike Godfrey** (Revenue Director & Commercial Strategist · Commercial & Revenue Management Strategist) — [What Rental Cars Taught Me About Selling Rooms: Overcoming Jargon & Owner Communication](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/What-Rental-Cars-Taught-Me-About-Selling-Rooms-e3fmjbl)
* **Episode 18: Heidi Gempel** (Revenue Director & Executive Coach · Founder & Executive Coach, HGE International) — [Two Habits That Will Change How You Lead: Executive Coaching & Psychological Safety](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Two-Habits-That-Will-Change-How-You-Lead--Heidi-Gempel-e3i4js1)
* **Episode 19: Stephen Fraser** (Consultant & Operations Leader · Head of Reservation Services, EVT Connect Hospitality) — [How to Navigate Career Changes: Adaptability & Cross-Functional Skills](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/How-to-Navigate-Career-Changes-Stephen-Fraser-e3jqpgr)
* **Episode 20: Matthew (Matt) Borger** (Tourism Chair & Sales Leader · Chairperson, Destination Port Stephens & Airlines / Partnerships Manager, Newcastle Airport) — [Hotel Sales Skills That Fill Planes: Commercial Alignment & Destination Marketing](https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Hotel-Sales-Skills-that-Fill-Planes-Matthew-Borger-e3lufab)

### The hospitality terminology standardisation register

Spoken hospitality interviews contain trade shorthand, financial acronyms, colloquialisms, and common transcription mishearings. To prevent language models from hallucinating or confusing metrics, we authored a canonical reference register ([`HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md`](https://github.com/haberlah/hotelier-huddle/blob/main/HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md)) defining 42 operational terms.

The register establishes clear distinctions between:
* **Rate and financial metrics:** RevPAR (gross room revenue divided by total rooms), Net RevPAR (net of OTA commissions and channel transaction fees), and GOPPAR (gross operating profit per available room).
* **Operational trade vocabulary:** "Day-trading rates" (obsessive, reactive hourly rate adjustments), "anecdata" (informal guest feedback picked up by housekeeping or front desk), "ROMO" (relief of missing out on competitor rate wars), and Mike Godfrey's concept of the "jargon junkie crap truck" (technical metrics dumped on unprepared owners).
* **Technical architecture:** Model Context Protocol (MCP), Small Language Models (SLMs), Retrieval-Augmented Generation (RAG), and enterprise data isolation boundaries.

### Seven thematic virtual panels

To allow users to consult the collective panel on specific operational challenges, the corpus synthesises dialogue into 7 virtual roundtables, each framed by Shannon's strategic moderator commentary:
1. **Panel 01: Commercial alignment and distribution:** Francis Purvey, Tamie Matthews, Matt Camp, Mike Godfrey, and Matt Borger debate why 100% occupancy is vanity, how 80–85% occupancy with rate integrity yields higher GOPPAR, eliminating screen day-trading, and holding 15-minute standing meetings with housekeeping.
2. **Panel 02: AI operating system and intelligent technology:** Francis Purvey, Dr David Haberlah, Andrew Taylor, Jasmine Xie, Jean-Christophe Buillet, and Heidi Gempel examine robotic check-in failures, enterprise data boundaries, MCP agentic protocols, and why AI increases the premium on human emotional intelligence.
3. **Panel 03: Crisis management and brand resilience:** Francis Purvey, Alexia Kalis, Eve Weatherburn, Michael Johnson, and Jean-Christophe Buillet share operational accounts of hurricane window blowouts, Tasmanian COVID border closures, brand equity as insurance against discounting, and competitors uniting for JobKeeper advocacy.
4. **Panel 04: Modern hotelier leadership and culture:** Alexia Kalis, Greg Brady, Michael Johnson, Kelley Wacher, Andrew Turner, and Heidi Gempel discuss GM floor-walking habits, leaving financials to controllers, the "Say Yes" promotion philosophy, psychological safety, and unlearning default crisis urgency.
5. **Panel 05: Non-linear careers and boardroom capabilities:** Joaquin D'Orazio, Michael Johnson, Kelley Wacher, Janet McBain, and Stephen Fraser analyse why hotel operational diplomacy translates directly to corporate boards, MBA validation, and executive leadership.
6. **Panel 06: Hotel development, precincts and asset strategy:** Eve Weatherburn, Andrew Taylor, Jean-Christophe Buillet, and Andrew Turner explore precinct masterplanning, converting windowless inventory into internal atrium gardens, strata-title management rights, and 23-year boutique owner-operator balance.
7. **Panel 07: Frontline guest experience and service craft:** Alexia Kalis, Tracy Martin, Greg Brady, Joaquin D'Orazio, and Jasmine Xie examine bespoke travel journeys, the formula of `value = benefit minus cost`, eliminating antiquated minibar inspections, and frontline curiosity.

### Five signature question knowledge bases

Across all 20 episodes, Shannon posed consistent questions that revealed foundational lessons:
1. **KB 01 (The Accidental Hotelier):** Tracing unexpected entrances into hospitality from teaching, law, geology, computing, and night audit shifts.
2. **KB 02 (Sales vs Revenue):** Dissecting the systemic misalignment between room volume and rate integrity across 9 commercial episodes.
3. **KB 03 (Advice to Younger Self):** Capturing career-defining guidance (such as Purvey's Monty Python mantra, Kalis's *"Fake it till you become it"*, Xie's *"Let your work speak for you"*, Turner's *"Master your job before telling others"*, and Godfrey's *"De-jargon your communication"*).
4. **KB 04 (Technology vs Human Touch):** Exploring where technology frees staff for genuine hospitality and where rigid automation alienates guests.
5. **KB 05 (The Final Toast Anthology):** All 20 closing toasts honouring the frontline workers, night auditors, room attendants, and kitchen crews who sustain hotels around the clock.

---

## Grounding AI responses in verbatim dialogue

To make *The Hotelier Huddle* genuinely useful to hoteliers and autonomous agents, every generated answer must remain faithful to what was actually spoken on the microphone. Pointing standard Retrieval-Augmented Generation (RAG) directly at raw conversational audio introduces three distinct retrieval failure modes:

1. **The introductory false positive:** Spoken interviews open with casual greetings, pleasantries, and career summaries. Keyword searches or naive semantic embeddings for terms like "hotel experience" or "revenue career" match the first five minutes of introductory chit-chat, bypassing the substantive operational principles delivered 35 minutes into the episode.
2. **Multi-turn dialogue dispersion:** In conversational speech, an operational principle is rarely delivered in a single self-contained sentence. The host introduces a commercial dilemma, the guest validates it with an operational war story, clarifies edge cases, and concludes with a strategic rule. Standard semantic chunkers (splitting text arbitrarily by character count) fracture this dialogue, separating the conclusion from the qualifying context.
3. **Colloquial terminology drift:** Conversational dialogue relies heavily on property-level slang, financial metaphors, and shorthand. Generic language models confuse distinct financial metrics—such as treating RevPAR (gross room revenue per available room) and Net RevPAR (net of OTA commissions and channel acquisition costs) as interchangeable—without domain-specific terminology grounding.

To solve these challenges and keep responses strictly grounded in the corpus, I developed a deterministic compilation pipeline (`build_derived_documents_verified.py`). Rather than delegating chunking to an opaque vector database, this pipeline extracts curated, complete multi-turn exchanges, preserves speaker diarisation, and validates every quote character-for-character against master transcripts. An automated GitHub Actions CI workflow enforces 100.0% verbatim fidelity on every repository commit.

---

## The Model Context Protocol (MCP) architecture

To allow hoteliers using AI interfaces such as Claude, ChatGPT, or Gemini to interrogate this knowledge base without data extraction friction, we implemented the Model Context Protocol (MCP), an open standard developed by [Anthropic (2024)](https://modelcontextprotocol.io).

The system runs across two production environments:
* **Local Python FastMCP runtime:** Implemented in `mcp_server/server.py` using Python 3.10+ and the official `mcp` SDK, enabling local IDE integration, terminal exploration, and offline use.
* **Cloudflare Edge Worker deployment:** A serverless TypeScript implementation running on Cloudflare's global edge network ([`https://hotelier-huddle-mcp.haberlah.workers.dev`](https://hotelier-huddle-mcp.haberlah.workers.dev)). The worker bundles the 2.57 MB compiled corpus directly into edge memory, delivering sub-50ms query responses worldwide without an external database. It supports Streamable HTTP (`POST /mcp`) and Server-Sent Events (`GET /sse`).

### MCP tools exposed to client models

The server exposes six dedicated tools directly into the model's reasoning loop:
* `list_episodes`: Returns metadata, guest bios, topics, and canonical Spotify URLs for all 20 episodes.
* `get_episode_transcript(episode_number)`: Retrieves the complete, timestamped verbatim transcript for any episode.
* `search_transcripts(query, max_results)`: Executes full-text search across all 1,842 turns with speaker and timestamp attribution.
* `query_thematic_council(council_id)`: Retrieves structured multi-turn debates from one of the 7 virtual panels.
* `get_hospitality_term(term)`: Returns canonical definitions, mishearings, and strategic context from the terminology register.
* `get_question_kb(question_id)`: Retrieves multi-episode perspectives on Shannon's 5 signature questions.

---

## Interrogating the corpus: a live demonstration

When hoteliers query an AI assistant connected to The Hotelier Huddle MCP server, they do not need to cite specific episode numbers or name individual interviewees. Instead, they present the authentic, high-friction dilemmas encountered in daily hotel operations. The AI assistant uses the underlying MCP tools to synthesise answers from verified dialogue.

Here is a live operational query executed against the production Cloudflare Edge Worker:

> **User Question:**  
> *"I want to use AI to improve my operations. What tools should I be considering?"*  
>  
> **Underlying Tool Execution:**  
> The model autonomously executes `query_thematic_council("ai_technology")` and `get_question_kb("q4")` ("Technology, AI and the Human Touch").

### Synthesised response

Based on querying the live *Hotelier Huddle* knowledge base, the panel explicitly warns against adopting generic "magic wand" AI software. The council draws a strict boundary: **automate back-office friction, but never automate away the frontline hospitality experience.**

When evaluating AI tools to improve hotel operations, the corpus points to four concrete architectural layers:

#### 1. Agentic Distribution Interfaces (Model Context Protocol / Agent-to-Payments)
* **The Problem:** Traditional hotel tech remains siloed behind legacy web booking engines designed solely for human eyeballs clicking on forms.
* **Tools to Consider:** Exposing hotel inventory, room attributes, and direct booking rails through **Model Context Protocol (MCP)** endpoints and Agent-to-Payments (A2P) protocols.
* **Corpus Insight:**
  > *"Foundation models—ChatGPT, Claude, Perplexity—are becoming the operating system. Instead of expecting a guest to browse ten OTA tabs or fill out a form on your website, guest agents will query inventory, negotiate constraints, and transact directly. Hotels that expose structured, trustworthy MCP endpoints will win direct bookings before the guest ever visits an aggregator."*  
  — **Dr David Haberlah**, *Episode 05: The AI Operating System is Coming: Are Hotels Ready?* [35:19–37:39]

#### 2. Internal Guest Knowledge Mining (Enterprise RAG & Small Language Models)
* **The Problem:** Over 80% of high-value guest context (dietary restrictions, past billing complaints, anniversary dates, room preferences) is trapped in unstructured emails, notes fields, and reservation remarks across fragmented PMS modules.
* **Tools to Consider:** Enterprise-grade **Retrieval-Augmented Generation (RAG)** and local/private **Small Language Models (SLMs)** integrated directly with the PMS/CRM.
* **Corpus Insight:**
  > *"The goldmine isn't in your structured database columns; it's buried in unstructured communication—the email chain before arrival, the concierge note. Deploying small, secure models within strict enterprise data boundaries lets you synthesize guest intent without leaking PII into consumer-facing public models."*  
  — **Dr David Haberlah**, *Episode 05* [05:44–07:41]

#### 3. Frontline Reservation & Sales Co-pilots
* **The Problem:** Reservation agents and sales coordinators spend excessive time compiling corporate contract history, checking calendar yield rules, and drafting routine correspondence.
* **Tools to Consider:** Context-aware **inbox and quotation co-pilots** that draft bespoke corporate RFP responses and surface historical folio spend in real time.
* **Corpus Insight:**
  > *"AI shouldn't talk to your high-value corporate client; it should arm your sales manager with their five-year stay history, banquet spend, and preferred terms within seconds so the salesperson can pick up the phone and close the deal."*  
  — **Jasmine Xie**, *Episode 11: The Revenue-Sales Dynamic* [16:47]  
  — Supported by **Andrew Taylor**, *Episode 10: Tech Integration & Commercial Strategy* [22:15]

#### 4. Explainable Revenue Decision-Support (Avoiding "System Hiding")
* **The Problem:** Modern AI revenue management systems evaluate ten times more variables than manual spreadsheets, leading to a dangerous operational failure mode where commercial teams abdicate responsibility to the algorithm.
* **Tools to Consider:** **Explainable Revenue Management Systems (RMS)** that provide transparent decision trees and demand attribution, rather than black-box automated rate pickers.
* **Corpus Insight:**
  > *"AI is a sparring partner, not an autopilot. The greatest risk we see today is 'system hiding'—revenue managers accepting an algorithmic rate drop or surge without understanding the underlying compression or flight data driving it. Choose tools that explain their working, and keep human judgement accountable for strategy."*  
  — **Heidi Gempel**, *Episode 18: Commercial Strategy & Boardroom Revenue* [14:30]

---

### The Panel's Core Governance Warning: The iPad Trap
When prioritising tools, the council highlights a cautionary case study from Florida:
> *"We once trialled removing the front reception and having guests check in on iPads to cut operational overhead. It was an unmitigated disaster and we pulled it immediately. Guests arriving after a delayed flight don't want an AI interface; they want empathy, eye contact, and human recognition. Automate the night audit reconciliation, automate the folio routing—keep the humans in the lobby."*  
— **Francis Purvey**, *Episode 01: The Foundation of Hotel Commercial Strategy* [31:13]  
— Reinforced by **Jean-Christophe Buillet**, *Episode 14: Asset Management & Operational Efficiency* [21:42]

---

### Summary Checklist for Tool Selection
1. **Does it respect enterprise data privacy?** Ensure guest PII stays within your tenant boundaries.
2. **Does it eliminate back-office paperwork?** Focus on reconciliation, night audit, and RFP drafting.
3. **Is the reasoning explainable?** Reject black-box systems where staff cannot explain why an action was taken.
4. **Does it protect front-of-house presence?** Never use AI to replace face-to-face service recovery or arrival welcomes.

---

## Setup guide: connecting your AI assistant to the huddle

Because the complete 20-episode knowledge base is deployed directly to Cloudflare’s global edge network, **you do not need to install Python, clone GitHub repositories, or manage databases** to interrogate the corpus. 

Any AI client that supports the Model Context Protocol (MCP) can connect to the live edge server in under sixty seconds.

### Method 1: Claude Desktop (Zero-install remote connection)

If you use Anthropic’s official [Claude Desktop](https://claude.ai/download) app, you can connect directly to the live Cloudflare Worker via `mcp-remote`:

1. Open your Claude Desktop configuration file:
   * **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   * **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the `hotelier-huddle` remote server:
   ```json
   {
     "mcpServers": {
       "hotelier-huddle": {
         "command": "npx",
         "args": [
           "-y",
           "mcp-remote",
           "https://hotelier-huddle-mcp.haberlah.workers.dev/sse"
         ]
       }
     }
   }
   ```
3. Restart Claude Desktop. A hammer icon will appear in the bottom-right corner showing all 6 tools active.

### Method 2: Cursor, Windsurf, or modern AI IDEs

Modern AI development environments support MCP endpoints natively through their graphical settings:

1. Open **Settings** → **MCP** (or **Features** → **MCP Servers**).
2. Click **Add New MCP Server**.
3. Set the fields:
   * **Name:** `hotelier-huddle`
   * **Type:** `SSE` (Server-Sent Events)
   * **Server URL:** `https://hotelier-huddle-mcp.haberlah.workers.dev/sse`
4. Click **Save**. The server connects immediately with zero local configuration.

### Method 3: Terminal agents (Claude Code CLI)

If you run terminal-based workflows using Anthropic’s Claude Code CLI, register the remote Streamable HTTP endpoint with a single command:

```bash
claude mcp add --transport http hotelier-huddle https://hotelier-huddle-mcp.haberlah.workers.dev/mcp
```

Verify that the connection is active:
```bash
claude mcp list
# hotelier-huddle: https://hotelier-huddle-mcp.haberlah.workers.dev/mcp (HTTP) - ✔ Connected
```

### Method 4: Local offline development (Python FastMCP)

For software engineers who want to audit the raw transcripts, run regression tests, or extend the tool suite offline, the repository includes a self-contained Python FastMCP implementation:

```bash
git clone https://github.com/haberlah/hotelier-huddle.git
cd hotelier-huddle
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python mcp_server/server.py
```

### What about ChatGPT, Gemini, and web-only users?

> **A note on platform compatibility:**  
> The Model Context Protocol is an open standard originated by Anthropic that is rapidly being adopted across developer tools (Cursor, Zed, Windsurf, Claude Code, LibreChat).  
> 
> * **ChatGPT (OpenAI):** The consumer web interface at `chatgpt.com` does not yet natively support direct MCP connections without an intermediary wrapper (such as LibreChat).  
> * **Gemini (Google):** While developers can connect the server to Gemini agentic SDKs and CLI harnesses, standard consumer accounts on `gemini.google.com` do not currently provide an MCP configuration panel.  
> 
> To consult the corpus today, we recommend using **Claude Desktop**, **Cursor**, or any open-source MCP client.

---

## Keeping the huddle open

In the opening episode of the series, Shannon observed that "AI, despite its perils and imperfections, can make us humans smarter and better providers of hospitality" (Episode 01 [00:00]). When we later spoke on Episode 05 about anxieties surrounding automation, she reminded me that technological shifts expand human craft rather than end it: "It wasn't the end of art at all. In fact, it was the beginning of new forms of art. It's always the beginning of new things, isn't it?" (Episode 05 [51:34]).

Shannon created *The Hotelier Huddle* so that emerging professionals could benefit from hard-won commercial experience without taking twenty years to learn it through trial and error. By preserving these conversations as an open-source, AI-addressable knowledge base, Heidi Egger and I have ensured that her final work remains active, accessible, and grounded in verified dialogue.

To protect Shannon's legacy from commercial exploitation, the entire project is hosted openly on [GitHub](https://github.com/haberlah/hotelier-huddle) under an ethical dual-licensing framework:
* **The knowledge base, transcripts, and derived virtual panels** are published under **Creative Commons (CC BY-NC-SA 4.0)**. This guarantees that Shannon's educational work remains permanently accessible to hoteliers, students, and researchers, while prohibiting commercial paywalling.
* **The software code, MCP servers, and deployment scripts** are open-sourced under the **MIT Licence**, allowing developers to integrate client connectors into operational workflows.
* **Engineering governance:** The repository follows open-source best practices, maintained with automated dependency scanning, a responsible disclosure [security policy](https://github.com/haberlah/hotelier-huddle/blob/main/SECURITY.md), and continuous integration enforcing 100% verbatim fidelity on every commit.

Whenever an emerging hotelier, revenue manager, or frontline team confronts an operational dilemma, Shannon Knapp and her council of 20 mentors are still in the room, ready to advise.

---

## References

Anthropic. (2024). *Model Context Protocol specification*. https://modelcontextprotocol.io

Douglas, J. (2026). *Shannon Knapp memorial tribute* [Video]. HSMAI Asia Pacific. https://asia.hsmai.org/wp-content/uploads/sites/12/2018/09/shannon-memorial-jackie.mp4

Goldstein, S. (2021). *The podcast cliff: Why 90% of podcasts fail before episode 21*. Amplifi Media. https://amplifimedia.com

Haberlah, D., & Egger, H. (2026). *The Hotelier Huddle: An open-source, AI-addressable hospitality knowledge base and Model Context Protocol server* [Computer software]. GitHub. https://github.com/haberlah/hotelier-huddle

HSMAI Asia Pacific. (2026). *Shannon Knapp, CHIA* [Faculty profile]. https://asia.hsmai.org/team/shannon-knapp/

Knapp, S. (Host). (2025, October 17). *The AI operating system is coming: Are hotels ready? With Dr David Haberlah* (Episode 05) [Audio podcast episode]. In *The Hotelier Huddle*. Spotify for Podcasters. https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/The-AI-Operating-System-is-Coming-Are-Hotels-Ready-e39l8k9

Knapp, S. (Host). (2026, January). *Are you revenue managing or day trading? With Matt Camp* (Episode 07) [Audio podcast episode]. In *The Hotelier Huddle*. Spotify for Podcasters. https://podcasters.spotify.com/pod/show/hotelier-huddle/episodes/Are-you-Revenue-Managing-or-Day-Trading-e389fm1

Knapp, S. (Host). (2025–2026). *The Hotelier Huddle* [Audio podcast]. Spotify for Podcasters. https://podcasters.spotify.com/pod/show/hotelier-huddle

Rachitsky, L. (2024). *Lenny's Podcast: Product, growth, and career conversations*. https://www.lennyspodcast.com

SiteMinder. (2024). *SiteMinder's changing traveller report 2025: The dynamic revenue revolution*. SiteMinder Limited. https://www.siteminder.com
