#!/home/deck/.openclaw/workspace/skills/scrapling/venv/bin/python3
"""
Solana Wallet Analyzer using Scrapling stealth mode
Scrapes Solscan for wallet analysis (anti-bot bypass)
"""
import sys
import json
import re
from scrapling.fetchers import StealthyFetcher

def analyze_wallet(wallet_address):
    """Scrape and analyze a Solana wallet from Solscan"""
    url = f"https://solscan.io/account/{wallet_address}"
    
    print(f"🔍 Fetching wallet data (stealth mode)...", file=sys.stderr)
    page = StealthyFetcher.fetch(
        url, 
        headless=True,
        network_idle=True,
        google_search=False
    )
    
    # Extract all text
    all_text = ' '.join(page.css('body *::text').getall())
    
    # Parse key metrics
    result = {
        "wallet": wallet_address,
        "url": url,
        "balances": {},
        "tokens": [],
        "activity": {}
    }
    
    # SOL balance
    sol_match = re.search(r'(\d+\.?\d*)\s*SOL Balance', all_text)
    if sol_match:
        result["balances"]["SOL"] = float(sol_match.group(1))
    
    # USD value
    usd_match = re.search(r'Total Value \$(\d+\.?\d*)', all_text)
    if usd_match:
        result["balances"]["USD"] = float(usd_match.group(1))
    
    # Token balance
    token_balance_match = re.search(r'Token Balance (\d+) Tokens \(\$ ([\d.]+) \)', all_text)
    if token_balance_match:
        result["balances"]["token_count"] = int(token_balance_match.group(1))
        result["balances"]["token_value_usd"] = float(token_balance_match.group(2))
    
    # BLOWFISH token (our token!)
    blowfish_match = re.search(r'([\d.]+[KMB]?)\s+BLOWFISH.*?\(\~?\$?([\d.]+)\)', all_text)
    if blowfish_match:
        result["tokens"].append({
            "symbol": "BLOWFISH",
            "amount": blowfish_match.group(1),
            "value_usd": float(blowfish_match.group(2))
        })
    
    # Recent transactions
    tx_pattern = r'(\w{88})\s+(\d+)\s+(hrs?|mins?|secs?)\s+ago\s+(\w+)'
    transactions = re.findall(tx_pattern, all_text)
    result["activity"]["recent_transactions"] = len(transactions)
    result["activity"]["latest_action"] = transactions[0][3] if transactions else None
    result["activity"]["time_ago"] = f"{transactions[0][1]} {transactions[0][2]}" if transactions else None
    
    # Gaming activity (Flip.gg)
    if "flip.gg" in all_text.lower():
        result["activity"]["gaming"] = "Active on Flip.gg"
    
    # DFlow swaps
    if "DFlow" in all_text:
        result["activity"]["defi"] = "Active swapper (DFlow)"
    
    return result

def format_report(result):
    """Format analysis result as human-readable report"""
    lines = []
    lines.append("=" * 60)
    lines.append("💼 SOLANA WALLET ANALYSIS")
    lines.append("=" * 60)
    lines.append(f"\n📍 Address: {result['wallet']}")
    lines.append(f"🔗 Solscan: {result['url']}")
    
    if result['balances']:
        lines.append("\n💰 BALANCES:")
        for key, value in result['balances'].items():
            if key == "SOL":
                lines.append(f"  💎 {value} SOL")
            elif key == "USD":
                lines.append(f"  💵 ${value} USD")
            elif key == "token_count":
                lines.append(f"  🪙 {value} tokens held")
            elif key == "token_value_usd":
                lines.append(f"     (~${value} total value)")
    
    if result['tokens']:
        lines.append("\n🔥 TOP TOKENS:")
        for token in result['tokens']:
            lines.append(f"  {token['symbol']}: {token['amount']} (~${token['value_usd']})")
    
    if result['activity']:
        lines.append("\n📊 ACTIVITY:")
        for key, value in result['activity'].items():
            if key == "recent_transactions":
                lines.append(f"  📝 {value} recent transactions")
            elif key == "latest_action":
                lines.append(f"  ⚡ Latest: {value}")
            elif key == "time_ago":
                lines.append(f"     ({value} ago)")
            elif key == "gaming":
                lines.append(f"  🎰 {value}")
            elif key == "defi":
                lines.append(f"  💱 {value}")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wallet_analyzer.py <wallet_address> [--json]", file=sys.stderr)
        sys.exit(1)
    
    wallet = sys.argv[1]
    json_output = "--json" in sys.argv
    
    try:
        result = analyze_wallet(wallet)
        
        if json_output:
            print(json.dumps(result, indent=2))
        else:
            print(format_report(result))
    
    except Exception as e:
        error = {
            "error": str(e),
            "type": type(e).__name__,
            "wallet": wallet
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)
