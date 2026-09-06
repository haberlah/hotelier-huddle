# Grounding hotel revenue management in verbatim dialogue: An open-source model context protocol corpus

**David Haberlah**  
*Published 6 September 2026*  

---

## Abstract

Hospitality revenue management has historically operated as an oral tradition. While academic literature provides normative mathematical formulations for yield optimisation, the daily mechanics of pricing discipline, commercial alignment, channel distribution costs, and owner governance are negotiated in property-level executive meetings and hallway huddles. When podcast host Shannon Knapp, CHIA, launched *The Hotelier Huddle* in September 2025, her objective was to bridge this gap: bringing together Australia's and the international sector's commercial leaders to examine how the profession must adapt to machine learning, automated distribution, and artificial intelligence. 

Following the open-knowledge model popularised in technology by podcasters such as Lenny Rachitsky (*Lenny's Podcast*), this project formalises Shannon's 20-episode archive into an open-source, machine-readable knowledge base. By pairing character-for-character transcript audits with the Model Context Protocol (MCP), we provide an interface that allows hoteliers, researchers, and autonomous software agents to query 250 years of collective operational wisdom directly from verified dialogue. This paper documents the rationale, architectural design, corpus statistics, licensing framework, and technical implementation of the corpus.

---

## The tacit knowledge gap in hotel commercial operations

Academic research into hotel revenue management frequently models pricing through linear programming, probabilistic demand distributions, and expected marginal seat revenue algorithms (Kimes, 1989; Weatherford & Bodily, 1992). While these mathematical abstractions underpin automated revenue management systems (RMS), they omit the human and organisational dynamics that govern physical properties.

On the hotel floor, commercial outcomes depend on resolving structural conflicts:
1. **The sales and revenue divide:** Directors of Sales and Marketing (DOSMs) are traditionally incentivised on gross room nights and volume, whereas Directors of Revenue Management (DORMs) are evaluated on average daily rate (ADR) and revenue per available room (RevPAR).
2. **Channel acquisition friction:** Securing short-term occupancy through online travel agencies (OTAs) incurs commission penalties ranging from 15% to 25%, frequently degrading net gross operating profit per available room (GOPPAR) despite high headline occupancy.
3. **Operational cost realities:** High room turnover imposes heavy variable labour costs on housekeeping and engineering departments—expenses that standard revenue algorithms fail to account for when recommending tactical rate cuts.

Because these operational realities are rarely codified in formal textbooks, junior hoteliers and independent operators often learn them through costly trial and error. The primary repository of commercial knowledge remains informal: shared anecdotes between general managers, mentorship discussions, and private post-mortem analyses of budget cycles.

---

## Shannon Knapp's contribution: modernising the profession

Throughout a career spanning senior commercial positions at Starwood Hotels & Resorts, her tenure as Senior Enterprise Sales Director (APAC) at SiteMinder, and her leadership of SKnapp Consulting, Shannon Knapp recognised both the power and the limitations of hospitality technology.

At SiteMinder, Knapp observed how cloud connectivity and channel management democratised distribution for tens of thousands of properties across the Asia-Pacific region (SiteMinder, 2024). Yet she also witnessed a persistent operational failure mode: hotel teams adopting complex digital systems without the underlying commercial discipline required to steer them. Operators treated software as an automated fix, adjusting rates hourly in response to competitor movements—a practice industry veteran Matt Camp terms commercial "day-trading"—rather than executing a coherent strategy.

When Knapp established *The Hotelier Huddle* in 2025, her stated ambition was to prepare the hospitality industry for an era of generative artificial intelligence and autonomous distribution. She understood that machine learning models would commoditise mechanical data analysis. If an algorithm can forecast unconstrained demand and recalculate rate hurdles instantaneously, a revenue manager's value shifts entirely to cross-functional influence, stakeholder persuasion, owner communication, and ethical leadership.

Across 20 episodes recorded between September 2025 and July 2026, Knapp convened 20 leaders representing boutique luxury retreats, international integrated resorts, corporate hotel chains, airline partnerships, and asset advisory firms. Her discussions did not skim promotional talking points; they explored specific operational breakdowns, hurricane recoveries, pandemic survival strategies, and the systemic challenges of aligning commercial incentives across property departments.

---

## The open knowledge precedent: from Lenny's Podcast to hotel management

In the technology sector, Lenny Rachitsky demonstrated the leverage of transforming episodic podcast audio into structured knowledge bases. Through *Lenny's Podcast*, Rachitsky interviewed hundreds of product, growth, and engineering leaders, releasing verbatim transcripts, searchable directory databases, and community-curated repositories (Rachitsky, 2024). This resource became an indispensable operational manual for technology practitioners worldwide, illustrating that long-form audio retains lasting educational utility when transcribed, indexed, and made programmatically accessible.

Hospitality has lacked an equivalent open-access reference repository. Proprietary benchmarking datasets (such as STR CoStar reports) provide historical occupancy and rate indices, but they offer zero visibility into the leadership decisions that produced those numbers. Commercial masterclasses and industry conferences remain restricted behind corporate training budgets or commercial paywalls.

By taking inspiration from open-source knowledge models, our project ensures that Knapp's recorded conversations do not remain trapped inside proprietary podcast platforms. By transcribing every dialogue turn, auditing the text against master audio, and releasing the resulting corpus under Creative Commons licensing, we establish a permanent, public standardisation register for hotel operational practice.

---

## Corpus architecture and empirical statistics

The corpus reflects 20 complete podcast episodes. To guarantee academic rigor, every audio recording was processed through multi-pass diarisation, aligned to minute-by-minute timestamps, and manually cross-checked against industry terminology.

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

The dataset captures the following metrics:
* **Episodes published:** 20 complete episodes.
* **Recording window:** 16 September 2025 to 11 July 2026.
* **Total runtime:** 14 hours, 48 minutes, 22 seconds of spoken dialogue.
* **Transcribed volume:** 234,180 words across 1,842 discrete speaker turns.
* **Industry contributors:** 20 guest experts spanning 8 operational disciplines (General Managers, Directors of Revenue, Directors of Sales, Technology Founders, Commercial Consultants, Asset Directors, Tourism Chairs, and Frontline Concierges).
* **Thematic Virtual Panels:** 7 multi-turn roundtables synthesizing debate across related operational domains.
* **Signature Question Knowledge Bases:** 5 cross-corpus repositories indexing Knapp's recurring inquiries across all 20 episodes.
* **Audited verbatim citations:** 458 character-for-character quotes validated against audio timestamps.

### Thematic virtual panel composition

To enable targeted research, the corpus synthesises dialogue across 7 thematic panels:
1. **Panel 01: Commercial and revenue management mastermind:** Purvey, Matthews, Camp, Godfrey, and Borger on shifting from vanity occupancy to net profitability (Net RevPAR, GOPPAR, TRevPAR), eliminating rate day-trading, and managing channel costs.
2. **Panel 02: AI operating system and intelligent hotel technology:** Purvey, Haberlah, Taylor, Xie, Buillet, and Gempel on enterprise data boundaries, open protocols, the failures of robotic iPad check-in, and protecting emotional intelligence.
3. **Panel 03: Crisis management and brand resilience:** Purvey, Kalis, Weatherburn, Johnson, and Buillet on Category-5 hurricane responses, Tasmanian border closures, brand equity as insurance, and industry solidarity.
4. **Panel 04: Modern hotelier leadership and culture:** Kalis, Brady, Johnson, Wacher, Turner, and Gempel on floor-walking habits, prioritising employee net promoter scores (eNPS), psychological safety, and unlearning default crisis urgency.
5. **Panel 05: Non-linear careers and boardroom capabilities:** D'Orazio, Johnson, Wacher, McBain, and Fraser on mastering frontline disciplines, night audit foundations, and translating hotel diplomacy into corporate directorships.
6. **Panel 06: Hotel development, precincts and asset strategy:** Weatherburn, Taylor, Buillet, and Turner on precinct masterplanning, converting windowless inventory into atrium gardens, strata-title dynamics, and boutique owner-operator balance.
7. **Panel 07: Frontline guest experience and service craft:** Kalis, Martin, Brady, D'Orazio, and Xie on bespoke travel journeys, the formula of `value = benefit minus cost`, eliminating antiquated minibar inspections, and frontline curiosity.

---

## Why standard retrieval-augmented generation fails on conversational transcripts

Deploying standard Retrieval-Augmented Generation (RAG) pipelines against unstructured conversational audio introduces systematic retrieval errors:

1. **The introductory false-positive:** Podcast interviews begin with informal pleasantries, introductions, and resume summaries. Keyword searches for terms like "revenue management career" or "hotel experience" match early greeting turns rather than substantive tactical answers delivered 35 minutes into the conversation.
2. **Multi-turn thought distribution:** Unlike textbook prose, spoken insights develop across several conversational turns. A host offers an observation, the guest affirms it, qualifies it with an anecdote, and concludes with an operational principle. Truncating retrieval to single-sentence chunks separates the insight from its qualifying context.
3. **Terminological distortion:** Conversational transcripts contain colloquialisms, mishearings, and industry acronyms. Without canonical terminology grounding, vector similarity search confuses distinct metrics such as RevPAR (revenue per available room), Net RevPAR (net of commission), and GOPPAR (gross operating profit per available room).

To resolve these failure modes, we constructed a deterministic compilation pipeline (`build_derived_documents_verified.py`). The pipeline maps specific, audited turn ranges into cohesive dialogue units, paired with a canonical dictionary (`HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md`) defining 42 industry terms. Automated continuous integration tests enforce a 100.0% character-for-character fidelity check against the raw transcript lines on every repository commit.

---

## The Model Context Protocol (MCP) architecture

To make this knowledge addressable by modern artificial intelligence systems without data extraction friction, we implemented the Model Context Protocol (MCP), an open standard developed by Anthropic (2024). MCP standardises how language models access external tools, prompts, and document resources.

We provide two production runtime environments:
1. **Local Python FastMCP runtime:** Built on Python 3.10+ and the official `mcp` library (`mcp_server/server.py`), enabling offline execution, local IDE integration, and script automation.
2. **Cloudflare Edge Worker deployment:** A serverless TypeScript implementation running on Cloudflare's global edge network (`https://hotelier-huddle-mcp.haberlah.workers.dev`). The worker bundles the verified 2.57 MB corpus (`corpus.json`) directly into edge memory, providing sub-50ms query responses worldwide without external database dependencies. It supports both Streamable HTTP (`POST /mcp`) and Server-Sent Events (`GET /sse`).

### MCP tools exposed to client models

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `list_episodes` | *none* | Returns metadata, guest bios, topics, and canonical Spotify URLs for all 20 episodes. |
| `get_episode_transcript` | `episode_number` (int) | Retrieves the complete, timestamped verbatim dialogue for any specific episode. |
| `search_transcripts` | `query` (str), `max_results` (int) | Executes full-text search across all 1,842 turns with speaker and timestamp attribution. |
| `query_thematic_council` | `council_id` (str) | Retrieves structured roundtable debates and takeaways from one of the 7 thematic panels. |
| `get_hospitality_term` | `term` (str) | Returns canonical definition, mishearings, and strategic context from the terminology register. |
| `get_question_kb` | `question_id` (str) | Retrieves multi-episode responses to one of Knapp's 5 core signature questions. |

---

## Repository governance and dual licensing

The project is hosted publicly on GitHub at [`https://github.com/haberlah/hotelier-huddle`](https://github.com/haberlah/hotelier-huddle).

To balance academic openness with intellectual property protection, the repository uses a dual-licensing structure:
* **The derived knowledge base, transcripts, and metadata** are licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Licence (CC BY-NC-SA 4.0)**. This licence guarantees that Shannon Knapp's educational legacy remains freely accessible to hoteliers, students, and researchers, while prohibiting commercial exploitation or paywalling by proprietary training vendors.
* **The software code, MCP servers, and automation tools** are licensed under the **MIT Licence**, allowing developers to freely integrate the client tools into open-source or proprietary workflows.

The repository adheres to open-source software engineering standards:
* **Security policy ([`SECURITY.md`](file:///Users/haberlah/Documents/hotelier%20huddle/hotelier%20huddle/SECURITY.md)):** Establishes private vulnerability reporting to David Haberlah with a 48-hour response SLA.
* **Automated dependency scanning ([`.github/dependabot.yml`](file:///Users/haberlah/Documents/hotelier%20huddle/hotelier%20huddle/.github/dependabot.yml)):** Weekly dependency monitoring across GitHub Actions, npm packages, and Python modules.
* **Hardened CI ([`.github/workflows/ci.yml`](file:///Users/haberlah/Documents/hotelier%20huddle/hotelier%20huddle/.github/workflows/ci.yml)):** Runs JSON validation, Python compilation, the 458-quote verbatim fidelity audit, and git diff checks under least-privilege `contents: read` permissions.

---

## Practical guide: connecting to the MCP knowledge base

Hoteliers, analysts, and developers can connect their preferred artificial intelligence environment to The Hotelier Huddle knowledge base using either remote edge connections or local Python execution.

### Method 1: connecting Claude Desktop (local FastMCP)

Edit your Claude Desktop configuration file:
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the local FastMCP server definition:

```json
{
  "mcpServers": {
    "hotelier-huddle": {
      "command": "/path/to/hotelier-huddle/.venv/bin/python3",
      "args": [
        "/path/to/hotelier-huddle/mcp_server/server.py"
      ]
    }
  }
}
```

### Method 2: connecting Gemini Desktop or web clients (remote SSE)

In the Gemini Desktop application or compatible MCP client, navigate to **Settings > MCP Servers** (or edit `~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "hotelier-huddle": {
      "serverUrl": "https://hotelier-huddle-mcp.haberlah.workers.dev/sse"
    }
  }
}
```

### Method 3: connecting the Claude Code CLI (remote HTTP)

In your terminal, register the remote Cloudflare endpoint directly into Claude Code:

```bash
claude mcp add --transport http hotelier-huddle https://hotelier-huddle-mcp.haberlah.workers.dev/mcp
```

Verify connection status:
```bash
claude mcp list
# Output: hotelier-huddle: https://hotelier-huddle-mcp.haberlah.workers.dev/mcp (HTTP) - ✔ Connected
```

---

## Sample queries for hoteliers and researchers

Once connected, hoteliers can interrogate the collective wisdom using natural language. Because tool calls are grounded in verified quotes, responses cite specific episode timestamps rather than generating synthetic generalisations:

### Query 1: Commercial strategy and occupancy targets
> *"An asset owner is demanding that our 180-room hotel achieve 100% occupancy next month by discounting our remaining inventory on Booking.com and Expedia. What specific warnings and operational alternatives do Tamie Matthews and Matt Camp provide regarding Net RevPAR and labour costs?"*

### Query 2: Sales and revenue alignment
> *"Our Director of Sales and Director of Revenue Management disagree on group corporate pricing for Q3. How does Francis Purvey suggest resolving this tension, and what meeting format does Shannon Knapp recommend to align the executive team?"*

### Query 3: Enterprise AI data boundaries
> *"We are evaluating autonomous guest communication agents for pre-arrival requests. What principles does Dr. David Haberlah articulate in Episode 05 regarding proprietary data boundaries, model context protocol standards, and preventing commercial data leakage?"*

---

## References

Anthropic. (2024). *Model Context Protocol specification*. https://modelcontextprotocol.io

Cross, R. G. (1997). *Revenue management: Hard-core tactics for market domination*. Broadway Books.

Kimes, S. E. (1989). The basics of yield management. *Cornell Hotel and Restaurant Administration Quarterly*, 30(3), 14–19. https://doi.org/10.1177/001088048903000307

Knapp, S. (Host). (2025–2026). *The Hotelier Huddle* [Audio podcast]. Spotify for Podcasters. https://podcasters.spotify.com/pod/show/hotelier-huddle

Rachitsky, L. (2024). *Lenny's Podcast: Product, growth, and career conversations*. https://www.lennyspodcast.com

SiteMinder. (2024). *SiteMinder's changing traveller report 2025: The dynamic revenue revolution*. SiteMinder Limited. https://www.siteminder.com

Weatherford, L. R., & Bodily, S. E. (1992). A taxonomy and review of nonlinear programming approaches to yield management. *Operations Research*, 40(5), 831–844. https://doi.org/10.1287/opre.40.5.831
