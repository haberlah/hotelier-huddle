"""
The Hotelier Huddle — Model Context Protocol (MCP) Server

Exposes the 20-episode Hotelier Huddle podcast knowledge base, 7 virtual panel councils,
5 signature question repositories, and the Hospitality Terminology Standardisation Register
as an AI-queryable MCP server using FastMCP.
"""

import os
import json
import re
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("hotelier-huddle", dependencies=["mcp"])

# Base Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.json")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
PANELS_DIR = os.path.join(BASE_DIR, "derived_knowledge_base", "virtual_panels")
QUESTIONS_DIR = os.path.join(BASE_DIR, "derived_knowledge_base", "question_knowledge_bases")
GLOSSARY_PATH = os.path.join(BASE_DIR, "HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md")

def load_index() -> Dict[str, Any]:
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"episodes": []}

# ---------------------------------------------------------------------------
# MCP Resources
# ---------------------------------------------------------------------------

@mcp.resource("hotelier://catalog")
def get_catalog() -> str:
    """Returns the full master catalog of all 20 episodes in JSON format."""
    return json.dumps(load_index(), indent=2)

@mcp.resource("hotelier://glossary")
def get_glossary() -> str:
    """Returns the complete Hospitality Terminology Standardisation Register."""
    if os.path.exists(GLOSSARY_PATH):
        with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return "Glossary not found."

@mcp.resource("hotelier://panels")
def get_panels_list() -> str:
    """Returns the list and descriptions of all 7 Thematic Virtual Panels."""
    matrix_path = os.path.join(BASE_DIR, "HOTELIER_HUDDLE_EXPERT_PANEL_MATRIX.md")
    if os.path.exists(matrix_path):
        with open(matrix_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Panel matrix not found."

# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_episodes(tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all 20 episodes of The Hotelier Huddle, optionally filtered by a topical tag
    (e.g., 'ai', 'revenue-management', 'leadership', 'sales', 'luxury-hotels').
    """
    catalog = load_index()
    episodes = catalog.get("episodes", [])
    if tag:
        tag_lower = tag.lower()
        episodes = [ep for ep in episodes if any(tag_lower in t.lower() for t in ep.get("tags", []))]
    
    return [
        {
            "episode_number": ep["episode_number"],
            "title": ep["title"],
            "guest": ep["guest"],
            "guest_organization": ep.get("guest_organization", ""),
            "date": ep["date"],
            "audio_duration": ep["audio_duration"],
            "word_count": ep["word_count"],
            "tags": ep.get("tags", []),
            "description": ep.get("description", "")
        }
        for ep in episodes
    ]

@mcp.tool()
def get_episode_transcript(episode_number: int) -> str:
    """
    Retrieve the full verbatim transcript of an episode by its episode number (1 to 20).
    """
    catalog = load_index()
    for ep in catalog.get("episodes", []):
        if ep["episode_number"] == episode_number:
            fpath = os.path.join(BASE_DIR, ep["filename"])
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    return f.read()
    return f"Episode {episode_number} transcript not found."

@mcp.tool()
def search_transcripts(query: str, guest: Optional[str] = None, tag: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search across all 20 podcast transcripts for specific terms, concepts, or quotes.
    Returns matching dialogue turns with timestamps, speaker names, and context.
    """
    catalog = load_index()
    target_eps = catalog.get("episodes", [])
    
    if guest:
        g_lower = guest.lower()
        target_eps = [ep for ep in target_eps if g_lower in ep["guest"].lower()]
    if tag:
        t_lower = tag.lower()
        target_eps = [ep for ep in target_eps if any(t_lower in t.lower() for t in ep.get("tags", []))]
        
    query_lower = query.lower()
    matches = []
    
    for ep in target_eps:
        fpath = os.path.join(BASE_DIR, ep["filename"])
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            
        for idx, line in enumerate(lines):
            m = re.match(r'^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*\*\*([^*]+?):\*\*\s*(.*)$', line.strip())
            if m:
                ts, spk, text = m.groups()
                if query_lower in text.lower():
                    matches.append({
                        "episode_number": ep["episode_number"],
                        "episode_title": ep["title"],
                        "guest": ep["guest"],
                        "timestamp": ts,
                        "speaker": spk,
                        "text": text
                    })
                    if len(matches) >= max_results:
                        return matches
                        
    return matches

@mcp.tool()
def query_thematic_council(council_id: str) -> str:
    """
    Retrieve synthesized dialogue from one of the 7 Virtual Councils:
    - 'commercial_alignment': Panel 01 (Sales, Revenue, Net RevPAR & Distribution)
    - 'ai_technology': Panel 02 (AI OS, Data Boundaries, SLMs vs LLMs & Human Touch)
    - 'crisis_resilience': Panel 03 (Hurricanes, COVID, Brand Reputation)
    - 'modern_leadership': Panel 04 (GM Leadership, Culture, Frontline Empowerment)
    - 'nonlinear_careers': Panel 05 (Transferable Skills, Night Audit to CEO)
    - 'asset_strategy': Panel 06 (Precincts, Wellness Revenue, Strata Models)
    - 'service_craft': Panel 07 (Frontline Empathy, Personalisation, Concierge)
    """
    mapping = {
        "commercial_alignment": "PANEL_01_Commercial_Alignment_Sales_vs_Revenue.md",
        "ai_technology": "PANEL_02_AI_Technology_and_the_Human_Touch.md",
        "crisis_resilience": "PANEL_03_Crisis_Management_Brand_Recovery_and_Resilience.md",
        "modern_leadership": "PANEL_04_Leadership_Culture_and_People_Over_Profit.md",
        "nonlinear_careers": "PANEL_05_Non_Linear_Careers_and_Boardroom_Skills.md",
        "asset_strategy": "PANEL_06_Hotel_Development_Precincts_and_Asset_Strategy.md",
        "service_craft": "PANEL_07_Frontline_Guest_Experience_and_Service_Craft.md"
    }
    
    fname = mapping.get(council_id.lower())
    if not fname:
        return f"Council '{council_id}' not found. Available councils: {list(mapping.keys())}"
        
    p_path = os.path.join(PANELS_DIR, fname)
    if os.path.exists(p_path):
        with open(p_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"Council document {fname} not found."

@mcp.tool()
def get_hospitality_term(term: str) -> Dict[str, str]:
    """
    Lookup any specialized hotel metric or system in the Hospitality Terminology Register
    (e.g., 'TRevPAR', 'Net RevPAR', 'GOPPAR', 'anecdata', 'day trading', 'RAG', 'AI OS', 'MLOS').
    """
    if not os.path.exists(GLOSSARY_PATH):
        return {"error": "Glossary file not found."}
        
    with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = rf'\|\s*\*\*([^*]*{re.escape(term)}[^*]*)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|\n]+)\|'
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        return {
            "term": m.group(1).strip(),
            "aliases_or_mishearings": m.group(2).strip(),
            "definition": m.group(3).strip(),
            "strategic_context": m.group(4).strip()
        }
        
    return {"message": f"Term '{term}' not found in the Hospitality Terminology Register."}

# ---------------------------------------------------------------------------
# MCP Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
def operational_consultation(challenge_description: str) -> str:
    """Prompt template to consult the 20 hoteliers on a commercial or operational challenge."""
    return f"""You are consulting the expert mastermind panel of The Hotelier Huddle (20 seasoned general managers, commercial directors, revenue leaders, and hotel technologists).
A hotelier is facing the following challenge:
"{challenge_description}"

Please analyze this challenge and provide concrete, actionable advice synthesized directly from relevant leaders in the Hotelier Huddle corpus (e.g. Tamie Matthews on Net RevPAR, Matt Camp on anecdata and rate stability, Dr. David Haberlah on AI data security, Greg Brady on frontline empowerment, or Michael Johnson on leadership).
Cite specific verbatim insights and timestamps wherever applicable."""

def main():
    mcp.run()

if __name__ == "__main__":
    main()
