# Contributing to The Hotelier Huddle Knowledge Base

We welcome contributions to improve transcript accuracy, expand the hospitality terminology register, or extend the Model Context Protocol (MCP) server tooling.

---

## Contribution Guidelines

1. **Verbatim Fidelity is Paramount:**
   Transcripts are faithful historical records of spoken conversation. Do not rephrase, embellish, or alter dialogue turns.
2. **Hospitality Terminology Standardisation:**
   Always consult [`HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md`](HOSPITALITY_TERMINOLOGY_STANDARDISATION_REGISTER.md) for canonical acronyms (*TRevPAR, Net RevPAR, GOPPAR, ADR, OTA, PMS, CRS, GDS, STR*).
3. **Turn Formatting Standard:**
   Speaker turns must strictly adhere to:
   ```markdown
   [MM:SS] **Speaker Name:** Dialogue text
   ```
   Do not insert timestamps mid-paragraph or mid-sentence.
4. **Verbatim Quote Synchronization:**
   If you modify a line in `transcripts/`, run:
   ```bash
   python3 build_derived_documents_verified.py
   ```
   This script regenerates the 7 Virtual Panels and 5 Question KBs and asserts that **all 340 quoted turns match 100% character-for-character**.
