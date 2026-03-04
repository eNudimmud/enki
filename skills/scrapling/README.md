# Scrapling Skill

Modern web scraping with adaptive element finding, anti-bot bypass, and AI-optimized content extraction.

## Quick Start

### Command Line

**Simple scraping:**
```bash
skills/scrapling/scripts/scrape.py 'https://example.com' --json
```

**Extract specific elements:**
```bash
skills/scrapling/scripts/scrape.py 'https://quotes.toscrape.com/' \
  --css '.quote .text::text' \
  --getall \
  --json
```

**Stealth mode (Cloudflare bypass):**
```bash
skills/scrapling/scripts/scrape.py 'https://protected-site.com' \
  --stealth \
  --solve-cloudflare \
  --css '.content'
```

**Adaptive mode (survives redesigns):**
```bash
skills/scrapling/scripts/scrape.py 'https://example.com' \
  --css '.product' \
  --adaptive \
  --getall
```

### Python Usage

```python
import sys
sys.path.insert(0, '/home/deck/.openclaw/workspace/skills/scrapling/venv/lib/python3.13/site-packages')

from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
data = page.css('.product .title::text').getall()
```

### MCP Server (Token Optimization)

**Start server:**
```bash
skills/scrapling/venv/bin/scrapling mcp --http --port 8000
```

**Configure in OpenClaw/Claude:**
```json
{
  "mcpServers": {
    "scrapling": {
      "url": "http://localhost:8000/mcp/v1"
    }
  }
}
```

**Benefits:**
- Extracts targeted content BEFORE sending to LLM
- Strips useless HTML → reduces tokens by large margin
- Faster responses + lower API costs

## Features

✅ **Adaptive element finding** — Auto-relocates elements after website redesigns  
✅ **Anti-bot bypass** — Handles Cloudflare Turnstile out of the box  
✅ **MCP Server** — Token-optimized extraction for AI  
✅ **Multiple fetchers** — HTTP (fast) or browser-based (stealth)  
✅ **Performance** — 2.02ms parsing (fastest in Python)  
✅ **Type hints** — Full coverage for IDE support

## Use Cases

1. **Token metrics monitoring** — Scrape Solana explorers (with stealth)
2. **Lore research** — NeukoAI community posts
3. **GitHub monitoring** — Issues/PRs when API rate-limited
4. **Weather/market data** — Adaptive tracking over time
5. **Content extraction for LLM** — Reduce token burn

## Limitations

**On SteamOS:**
- ⚠️ System dependencies failed (sudo required)
- ✅ HTTP fetcher works perfectly
- ⚠️ Stealth fetcher untested (may work despite warnings)

**Legal:**
- Respect robots.txt and ToS
- Educational/research use only
- Cloudflare bypass may violate some site policies

## Performance

- Parsing: **2.02ms** (vs BS4: 1584ms = 784x slower)
- Adaptive finding: **2.39ms** (vs AutoScraper: 12.45ms = 5x slower)
- HTTP/3 support + TLS fingerprint spoofing

## Documentation

- GitHub: https://github.com/D4Vinci/Scrapling
- Docs: https://scrapling.readthedocs.io
- Version: 0.4.1

## Philosophy

**Grey mastery.** Learn to audit data, bypass restrictions when necessary for legitimate research, but always respect ethics and law.

Part of the E*NKI sovereignty toolkit — tools that empower, not extract.
