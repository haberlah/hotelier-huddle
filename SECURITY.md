# Security Policy

## Supported Versions

The Hotelier Huddle project is actively maintained as an open-source knowledge repository and Model Context Protocol (MCP) service. The following versions receive active maintenance and security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security and integrity of this repository, its derived datasets, and its MCP endpoints seriously.

If you believe you have found a security vulnerability in the repository code, Cloudflare Edge Worker, or MCP server:

1. **Do not disclose the issue publicly** in GitHub Issues, Discussions, or pull requests.
2. **Contact the maintainer privately:** Send an email to **David Haberlah** at [david@bellaslainte.com](mailto:david@bellaslainte.com) with the subject line `[SECURITY] The Hotelier Huddle - Vulnerability Report`.
3. **Include details:**
   * A clear description of the vulnerability.
   * Steps to reproduce or proof-of-concept payload.
   * Potential impact on users, edge workers, or data privacy.

## Response Timeline

* **Initial Acknowledgment:** Within 48 hours of receipt.
* **Assessment & Remediation:** We will assess the severity, validate the report, and prepare a fix within 7 business days.
* **Public Disclosure:** Coordinated release and CVE attribution (if applicable) following deployment of the fix.

## Scope & Guidelines

* **In Scope:**
  * Cloudflare Worker endpoint security (`https://hotelier-huddle-mcp.haberlah.workers.dev`)
  * Model Context Protocol (MCP) server implementations (`mcp_server/` and `cloudflare_worker/`)
  * Data hygiene, secrets leakage, and dependency vulnerabilities
* **Out of Scope:**
  * Third-party podcast platforms (Spotify, Apple Podcasts, Anchor)
  * Denial-of-service attacks against Cloudflare edge infrastructure
