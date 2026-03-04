# Scrapling Skill - Advanced Web Scraping

## Overview

Scrapling is a modern web scraping framework with:
- **Adaptive element finding** — Survives website redesigns
- **Anti-bot bypass** — Handles Cloudflare Turnstile
- **MCP Server** — Token-optimized content extraction for AI
- **Multiple fetchers** — HTTP (fast) or browser-based (stealth)

## Installation

Already installed in venv at `~/.openclaw/workspace/skills/scrapling/venv/`

**Dependencies:**
- Python 3.10+
- Chromium browser (installed in `~/.cache/ms-playwright/`)
- MCP support enabled via `scrapling[ai]`

## Usage Patterns

### 1. Simple HTTP Scraping (Fast)

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
data = page.css('.product .title::text').getall()
```

**Use when:**
- No anti-bot protection
- Static content
- Speed matters

### 2. Adaptive Mode (Survives Redesigns)

```python
from scrapling.fetchers import Fetcher

# First scrape - save element locations
page = Fetcher.get('https://example.com')
products = page.css('.product', auto_save=True)

# Later, after website changes
page2 = Fetcher.get('https://example.com')
products2 = page2.css('.product', adaptive=True)  # Auto-relocates!
```

**Use when:**
- Monitoring long-term
- Website changes frequently

### 3. Stealth Mode (Bypass Anti-Bot)

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch('https://protected-site.com', 
                             headless=True, 
                             solve_cloudflare=True)
data = page.css('.content').get()
```

**Use when:**
- Cloudflare protected
- Anti-bot systems detected
- Need browser fingerprinting

### 4. MCP Server (Token-Optimized for AI)

**Start server:**
```bash
venv/bin/scrapling mcp --http --port 8000
```

**Features:**
- Extracts targeted content BEFORE sending to LLM
- Strips useless HTML tags
- Reduces token consumption significantly
- Compatible with Claude Desktop, VS Code Copilot

**Use when:**
- Processing large pages
- Want to reduce API costs
- Need structured extraction

## Command Reference

**Interactive shell:**
```bash
venv/bin/scrapling shell
```

**Direct extraction (no code):**
```bash
venv/bin/scrapling extract get 'https://example.com' content.md --css-selector '.main'
```

## Performance

- Parsing: **2.02ms** (baseline, fastest)
- Adaptive finding: **2.39ms** (~5x faster than AutoScraper)
- HTTP requests: TLS fingerprint spoofing, HTTP/3 support

## Limitations

**On SteamOS:**
- ⚠️ Browser system deps failed (sudo required)
- ✅ HTTP fetcher works perfectly
- ⚠️ Stealth/Dynamic fetchers untested (may work despite warnings)
- ✅ MCP server functional

**General:**
- Respect robots.txt
- Cloudflare bypass may violate ToS
- Educational/research use only

## Integration Ideas

1. **Replace web_fetch for complex scraping**
2. **MCP server for token reduction** (priority)
3. **Monitoring skill** — Adaptive mode for long-term tracking
4. **Token metrics scraper** — Solana explorers (with stealth)
5. **Lore research** — NeukoAI community posts

## References

- Repo: https://github.com/D4Vinci/Scrapling
- Docs: https://scrapling.readthedocs.io
- Latest: v0.4.1
- Installed: `~/.openclaw/workspace/skills/scrapling/`

---

**Philosophy alignment:** Grey mastery tool. Learn to audit data, bypass restrictions when necessary, but always respect the law and ethics.
