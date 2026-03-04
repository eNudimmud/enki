#!/home/deck/.openclaw/workspace/skills/scrapling/venv/bin/python3
"""
Test Scrapling stealth mode on Solscan - Simplified
"""
from scrapling.fetchers import StealthyFetcher

wallet = "4jRDWrm2pTxMDyX8iyGAuVGpvcqM1ms4UytSvjYB4wpF"
url = f"https://solscan.io/account/{wallet}"

print(f"🎯 Analyzing wallet: {wallet}\n")
print(f"🌐 URL: {url}\n")

print("Loading with headless browser (stealth mode)...")
page = StealthyFetcher.fetch(
    url, 
    headless=True,
    network_idle=True,
    google_search=False
)

print(f"✓ Page loaded: {page.css('title::text').get()}\n")

# Extract ALL text content from body
all_elements = page.css('body *::text').getall()
all_text = ' '.join(all_elements)

print(f"📊 Total text content: {len(all_text)} chars")
print(f"📊 Elements extracted: {len(all_elements)}")

# Find balance info
print("\n" + "=" * 60)
print("💰 WALLET ANALYSIS")
print("=" * 60)

import re

# Look for SOL balance
sol_pattern = r'(\d+\.?\d*)\s*SOL'
sol_balances = re.findall(sol_pattern, all_text)
if sol_balances:
    print(f"\n💎 SOL Balance: {sol_balances[0]} SOL")

# Look for USD value
usd_pattern = r'\$(\d+\.?\d*[KMB]?)'
usd_values = re.findall(usd_pattern, all_text)
if usd_values:
    print(f"💵 USD Value: ${usd_values[0]}")

# Look for token count
token_count_pattern = r'(\d+)\s+Token'
token_counts = re.findall(token_count_pattern, all_text)
if token_counts:
    print(f"🪙 Tokens held: {token_counts[0]}")

# Look for transaction count
tx_pattern = r'(\d+)\s+transaction'
tx_counts = re.findall(tx_pattern, all_text, re.IGNORECASE)
if tx_counts:
    print(f"📝 Transactions: {tx_counts[0]}")

# Show raw content sample (first matches)
print("\n" + "=" * 60)
print("📄 RAW DATA SAMPLE (first 1500 chars)")
print("=" * 60)
print(all_text[:1500])

# Save full content for debugging
with open('/tmp/solscan_content.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)
print(f"\n💾 Full content saved to /tmp/solscan_content.txt")

