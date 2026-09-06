/**
 * The Hotelier Huddle — Model Context Protocol (MCP) Cloudflare Worker
 * 
 * Provides global, low-latency MCP access to the 20-episode Hotelier Huddle podcast archive,
 * the Hospitality Terminology Register, and the 7 Virtual Panel Councils.
 */

import corpusData from "./corpus.json";

interface Episode {
  episode_number: number;
  title: string;
  guest: string;
  guest_title?: string;
  guest_organization?: string;
  date: string;
  audio_duration: string;
  word_count: number;
  tags?: string[];
  description?: string;
}

interface SpokenTurn {
  episode_number: number;
  episode_title: string;
  guest: string;
  tags?: string[];
  timestamp: string;
  speaker: string;
  text: string;
}

interface GlossaryTerm {
  term: string;
  aliases_or_mishearings: string;
  definition: string;
  strategic_context: string;
}

interface Corpus {
  index: {
    podcast_name: string;
    host: string;
    producer: string;
    curator?: string;
    dedication?: string;
    episodes_count: number;
    episodes: Episode[];
  };
  glossary_raw: string;
  glossary_terms: GlossaryTerm[];
  panels: Record<string, string>;
  questions: Record<string, string>;
  transcripts: Record<string, string>;
  turns: SpokenTurn[];
}

const corpus: Corpus = corpusData as unknown as Corpus;

// ---------------------------------------------------------------------------
// Tool Implementations
// ---------------------------------------------------------------------------

function listEpisodes(tag?: string): any[] {
  let episodes = corpus.index.episodes || [];
  if (tag) {
    const tLower = tag.toLowerCase();
    episodes = episodes.filter((ep) =>
      ep.tags?.some((t) => t.toLowerCase().includes(tLower))
    );
  }
  return episodes.map((ep) => ({
    episode_number: ep.episode_number,
    title: ep.title,
    guest: ep.guest,
    guest_organisation: ep.guest_organization || "",
    date: ep.date,
    audio_duration: ep.audio_duration,
    word_count: ep.word_count,
    tags: ep.tags || [],
    description: ep.description || ""
  }));
}

function getEpisodeTranscript(episodeNumber: number): string {
  const transcript = corpus.transcripts[String(episodeNumber)];
  if (transcript) {
    return transcript;
  }
  return `Episode ${episodeNumber} transcript not found. Available episodes: 1 to 20.`;
}

function searchTranscripts(
  query: string,
  guest?: string,
  tag?: string,
  maxResults = 5
): any[] {
  const qLower = query.toLowerCase();
  const gLower = guest ? guest.toLowerCase() : null;
  const tLower = tag ? tag.toLowerCase() : null;

  const matches: any[] = [];
  for (const turn of corpus.turns) {
    if (gLower && !turn.guest.toLowerCase().includes(gLower)) {
      continue;
    }
    if (tLower && !turn.tags?.some((t) => t.toLowerCase().includes(tLower))) {
      continue;
    }
    if (turn.text.toLowerCase().includes(qLower)) {
      matches.push({
        episode_number: turn.episode_number,
        episode_title: turn.episode_title,
        guest: turn.guest,
        timestamp: turn.timestamp,
        speaker: turn.speaker,
        text: turn.text
      });
      if (matches.length >= maxResults) {
        break;
      }
    }
  }
  return matches;
}

function queryThematicCouncil(councilId: string): string {
  const cLower = councilId.toLowerCase();
  const content = corpus.panels[cLower];
  if (content) {
    return content;
  }
  return `Council '${councilId}' not found. Available councils: ${Object.keys(
    corpus.panels
  ).join(", ")}`;
}

function getQuestionKb(questionId: string): string {
  const cleanId = questionId.toLowerCase().replace(/^kb_/, "");
  const content = corpus.questions[cleanId];
  if (content) {
    return content;
  }
  return `Question KB '${questionId}' not found. Available question IDs: q1, q2, q3, q4, q5.`;
}

function getHospitalityTerm(term: string): any {
  const tLower = term.toLowerCase();
  const found = corpus.glossary_terms.find(
    (g) =>
      g.term.toLowerCase().includes(tLower) ||
      g.aliases_or_mishearings.toLowerCase().includes(tLower)
  );

  if (found) {
    return found;
  }
  return {
    message: `Term '${term}' not found in the Hospitality Terminology Register.`
  };
}

// ---------------------------------------------------------------------------
// MCP Protocol Definitions
// ---------------------------------------------------------------------------

const MCP_TOOLS = [
  {
    name: "list_episodes",
    description:
      "List all 20 episodes of The Hotelier Huddle, optionally filtered by a topical tag (e.g. 'ai', 'revenue-management', 'leadership', 'sales', 'luxury-hotels').",
    inputSchema: {
      type: "object",
      properties: {
        tag: {
          type: "string",
          description: "Optional topic tag to filter episodes by"
        }
      }
    }
  },
  {
    name: "get_episode_transcript",
    description:
      "Retrieve the complete verbatim transcript of an episode by its episode number (1 to 20).",
    inputSchema: {
      type: "object",
      properties: {
        episode_number: {
          type: "number",
          description: "Episode number (1 to 20)"
        }
      },
      required: ["episode_number"]
    }
  },
  {
    name: "search_transcripts",
    description:
      "Search across all 20 podcast transcripts for specific terms, operational concepts, or quotes. Returns matching dialogue turns with timestamps, speaker names, and context.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query or concept" },
        guest: { type: "string", description: "Optional filter by guest name" },
        tag: { type: "string", description: "Optional filter by topic tag" },
        max_results: {
          type: "number",
          description: "Maximum number of results to return (default 5)",
          default: 5
        }
      },
      required: ["query"]
    }
  },
  {
    name: "query_thematic_council",
    description:
      "Retrieve synthesized dialogue from one of the 7 Virtual Councils: 'commercial_alignment', 'ai_technology', 'crisis_resilience', 'modern_leadership', 'nonlinear_careers', 'asset_strategy', 'service_craft'.",
    inputSchema: {
      type: "object",
      properties: {
        council_id: {
          type: "string",
          description: "Council identifier (e.g. 'commercial_alignment', 'ai_technology')"
        }
      },
      required: ["council_id"]
    }
  },
  {
    name: "get_hospitality_term",
    description:
      "Look up any specialized hotel metric or system in the Hospitality Terminology Register (e.g. 'TRevPAR', 'Net RevPAR', 'GOPPAR', 'Anecdata', 'Day Trading', 'RAG', 'AI OS', 'MLOS').",
    inputSchema: {
      type: "object",
      properties: {
        term: {
          type: "string",
          description: "Term or acronym to search"
        }
      },
      required: ["term"]
    }
  },
  {
    name: "get_question_kb",
    description:
      "Retrieve one of the 5 signature question knowledge bases across the corpus: 'q1' (Accidental Hotelier / Origins), 'q2' (Sales vs Revenue / Commercial Alignment), 'q3' (Advice to Emerging Hoteliers & Younger Self), 'q4' (Technology, AI vs Human Touch), 'q5' (Final Toast Anthology).",
    inputSchema: {
      type: "object",
      properties: {
        question_id: {
          type: "string",
          description: "Question identifier: 'q1', 'q2', 'q3', 'q4', or 'q5' (or 'kb_q1' etc.)"
        }
      },
      required: ["question_id"]
    }
  }
];

const MCP_RESOURCES = [
  {
    uri: "hotelier://catalog",
    name: "Master Catalog",
    description: "Full catalog of all 20 episodes with metadata, tags, and word counts in JSON.",
    mimeType: "application/json"
  },
  {
    uri: "hotelier://glossary",
    name: "Hospitality Terminology Register",
    description: "Canonical industry glossary of 35 hospitality, revenue, and AI terms.",
    mimeType: "text/markdown"
  },
  {
    uri: "hotelier://panels",
    name: "Virtual Panel Matrix",
    description: "Structure and panelist mappings for all 7 Virtual Panel Councils.",
    mimeType: "text/markdown"
  }
];

const MCP_PROMPTS = [
  {
    name: "operational_consultation",
    description:
      "Consult the 20 hoteliers of The Hotelier Huddle as an advisory council on an operational or commercial challenge.",
    arguments: [
      {
        name: "challenge_description",
        description: "Description of the operational, commercial, or leadership dilemma",
        required: true
      }
    ]
  }
];

// ---------------------------------------------------------------------------
// JSON-RPC Message Dispatcher
// ---------------------------------------------------------------------------

function handleJsonRpc(req: any): any {
  const { id, method, params } = req;

  // Notification (no ID)
  if (id === undefined && method?.startsWith("notifications/")) {
    return null;
  }

  switch (method) {
    case "initialize":
      return {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: {},
            resources: {},
            prompts: {}
          },
          serverInfo: {
            name: "hotelier-huddle",
            version: "1.0.0"
          }
        }
      };

    case "ping":
      return { jsonrpc: "2.0", id, result: {} };

    case "tools/list":
      return { jsonrpc: "2.0", id, result: { tools: MCP_TOOLS } };

    case "tools/call": {
      const toolName = params?.name;
      const args = params?.arguments || {};
      let resultText = "";

      if (toolName === "list_episodes") {
        resultText = JSON.stringify(listEpisodes(args.tag), null, 2);
      } else if (toolName === "get_episode_transcript") {
        resultText = getEpisodeTranscript(Number(args.episode_number));
      } else if (toolName === "search_transcripts") {
        const matches = searchTranscripts(
          args.query,
          args.guest,
          args.tag,
          args.max_results ? Number(args.max_results) : 5
        );
        resultText = JSON.stringify(matches, null, 2);
      } else if (toolName === "query_thematic_council") {
        resultText = queryThematicCouncil(args.council_id);
      } else if (toolName === "get_hospitality_term") {
        resultText = JSON.stringify(getHospitalityTerm(args.term), null, 2);
      } else if (toolName === "get_question_kb") {
        resultText = getQuestionKb(args.question_id);
      } else {
        return {
          jsonrpc: "2.0",
          id,
          error: { code: -32601, message: `Tool '${toolName}' not found.` }
        };
      }

      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [{ type: "text", text: resultText }]
        }
      };
    }

    case "resources/list":
      return { jsonrpc: "2.0", id, result: { resources: MCP_RESOURCES } };

    case "resources/read": {
      const uri = params?.uri;
      let text = "";
      let mimeType = "text/plain";

      if (uri === "hotelier://catalog") {
        text = JSON.stringify(corpus.index, null, 2);
        mimeType = "application/json";
      } else if (uri === "hotelier://glossary") {
        text = corpus.glossary_raw;
        mimeType = "text/markdown";
      } else if (uri === "hotelier://panels") {
        text = `# Virtual Panel Matrix\n\nAvailable Councils:\n` +
          Object.keys(corpus.panels).map(p => `* ${p}`).join("\n");
        mimeType = "text/markdown";
      } else {
        return {
          jsonrpc: "2.0",
          id,
          error: { code: -32002, message: `Resource '${uri}' not found.` }
        };
      }

      return {
        jsonrpc: "2.0",
        id,
        result: {
          contents: [{ uri, mimeType, text }]
        }
      };
    }

    case "prompts/list":
      return { jsonrpc: "2.0", id, result: { prompts: MCP_PROMPTS } };

    case "prompts/get": {
      const promptName = params?.name;
      if (promptName === "operational_consultation") {
        const challenge = params?.arguments?.challenge_description || "Hospitality operational challenge";
        return {
          jsonrpc: "2.0",
          id,
          result: {
            description: "Consult the 20 hoteliers of The Hotelier Huddle",
            messages: [
              {
                role: "user",
                content: {
                  type: "text",
                  text: `You are consulting the expert mastermind panel of The Hotelier Huddle (20 seasoned general managers, commercial directors, revenue leaders, and hotel technologists).\nA hotelier is facing the following challenge:\n"${challenge}"\n\nPlease analyze this challenge and provide concrete, actionable advice synthesized directly from relevant leaders in the Hotelier Huddle corpus. Cite specific verbatim insights and timestamps wherever applicable.`
                }
              }
            ]
          }
        };
      }
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Prompt '${promptName}' not found.` }
      };
    }

    default:
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method '${method}' not implemented.` }
      };
  }
}

// ---------------------------------------------------------------------------
// Worker Request Handler
// ---------------------------------------------------------------------------

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
  "Access-Control-Max-Age": "86400"
};

export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // 1. Handle CORS Preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // 2. Streamable HTTP MCP Endpoint (/mcp, /, or /sse)
    if (
      (url.pathname === "/mcp" || url.pathname === "/" || url.pathname === "/sse") &&
      request.method === "POST"
    ) {
      try {
        const body = await request.json();
        const response = handleJsonRpc(body);
        if (response === null) {
          return new Response(null, { status: 204, headers: CORS_HEADERS });
        }
        return new Response(JSON.stringify(response), {
          headers: {
            ...CORS_HEADERS,
            "Content-Type": "application/json"
          }
        });
      } catch (err: any) {
        return new Response(
          JSON.stringify({
            jsonrpc: "2.0",
            id: null,
            error: { code: -32700, message: "Parse error: " + err.message }
          }),
          {
            status: 400,
            headers: {
              ...CORS_HEADERS,
              "Content-Type": "application/json"
            }
          }
        );
      }
    }

    // 2b. Streamable HTTP GET SSE stream for notifications & keep-alive
    if (
      (url.pathname === "/mcp" || url.pathname === "/") &&
      request.method === "GET" &&
      request.headers.get("Accept")?.includes("text/event-stream")
    ) {
      const { readable, writable } = new TransformStream();
      const writer = writable.getWriter();
      const encoder = new TextEncoder();

      writer.write(encoder.encode(`: connected\n\n`));

      return new Response(readable, {
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive"
        }
      });
    }

    // 3. Server-Sent Events Endpoint (/sse)
    if (url.pathname === "/sse" && request.method === "GET") {
      const sessionId = crypto.randomUUID();
      const endpointUrl = `${url.origin}/message?sessionId=${sessionId}`;

      const { readable, writable } = new TransformStream();
      const writer = writable.getWriter();
      const encoder = new TextEncoder();

      // Send initial endpoint event
      writer.write(encoder.encode(`event: endpoint\ndata: ${endpointUrl}\n\n`));

      return new Response(readable, {
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive"
        }
      });
    }

    // 4. SSE Message Posting Endpoint (/message)
    if (url.pathname === "/message" && request.method === "POST") {
      try {
        const body = await request.json();
        const response = handleJsonRpc(body);
        return new Response(JSON.stringify(response), {
          headers: {
            ...CORS_HEADERS,
            "Content-Type": "application/json"
          }
        });
      } catch (err: any) {
        return new Response(
          JSON.stringify({
            jsonrpc: "2.0",
            id: null,
            error: { code: -32700, message: "Parse error: " + err.message }
          }),
          {
            status: 400,
            headers: { ...CORS_HEADERS, "Content-Type": "application/json" }
          }
        );
      }
    }

    // 5. Friendly Web Landing Page (GET /)
    const hostUrl = url.origin;
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Hotelier Huddle — MCP Knowledge Base</title>
  <style>
    :root {
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --gold: #d29922;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 20px;
    }
    h1, h2, h3 { color: var(--heading); }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      margin: 20px 0;
    }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      background: #238636;
      color: #fff;
    }
    pre {
      background: #000;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-size: 13px;
    }
    code { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }
    .quote {
      border-left: 3px solid var(--gold);
      padding-left: 16px;
      font-style: italic;
      color: #8b949e;
    }
  </style>
</head>
<body>
  <h1>The Hotelier Huddle MCP Server</h1>
  <p><span class="badge">Live & Operational</span> Cloudflare Edge Worker</p>
  
  <div class="card quote">
    <strong>Homage to the legacy of Shannon Knapp, CHIA</strong><br>
    This repository and MCP server are dedicated as an homage to the legacy of Shannon Knapp, CHIA, who until her last breath was passionate about advancing the hotel profession alongside her closest friends and industry peers. Produced by Heidi Egger, curated by Dr David Haberlah.
  </div>

  <div class="card">
    <h2>Connect with Claude Desktop or Cursor</h2>
    <p>Add the following configuration to your <code>claude_desktop_config.json</code>:</p>
    <pre><code>{
  "mcpServers": {
    "hotelier-huddle": {
      "url": "${hostUrl}/mcp"
    }
  }
}</code></pre>
  </div>

  <div class="card">
    <h2>Available MCP Tools</h2>
    <ul>
      <li><code>list_episodes(tag?)</code> — Catalog of all 20 episodes.</li>
      <li><code>get_episode_transcript(episode_number)</code> — Full verbatim transcript.</li>
      <li><code>search_transcripts(query, guest?, tag?, max_results?)</code> — Search across 2,409 spoken turns.</li>
      <li><code>query_thematic_council(council_id)</code> — Access 7 virtual panel roundtables.</li>
      <li><code>get_hospitality_term(term)</code> — Hospitality terminology lookup.</li>
    </ul>
    <h2>Available Resources</h2>
    <ul>
      <li><code>hotelier://catalog</code> — Master catalog JSON.</li>
      <li><code>hotelier://glossary</code> — Complete terminology register.</li>
      <li><code>hotelier://panels</code> — Virtual panel council matrix.</li>
    </ul>
  </div>

  <p>GitHub Repository: <a href="https://github.com/haberlah/hotelier-huddle" target="_blank">github.com/haberlah/hotelier-huddle</a></p>
</body>
</html>`;

    return new Response(html, {
      headers: { ...CORS_HEADERS, "Content-Type": "text/html; charset=utf-8" }
    });
  }
};
