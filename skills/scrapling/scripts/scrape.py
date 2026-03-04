#!/home/deck/.openclaw/workspace/skills/scrapling/venv/bin/python3
"""
Scrapling wrapper for OpenClaw
Usage: scrape.py <url> [options]
"""
import sys
import json
import argparse
from scrapling.fetchers import Fetcher, StealthyFetcher

def main():
    parser = argparse.ArgumentParser(description='Scrape a URL with Scrapling')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--css', help='CSS selector to extract')
    parser.add_argument('--xpath', help='XPath selector to extract')
    parser.add_argument('--text', action='store_true', help='Extract text content only')
    parser.add_argument('--html', action='store_true', help='Extract HTML content')
    parser.add_argument('--stealth', action='store_true', help='Use StealthyFetcher (browser-based)')
    parser.add_argument('--headless', action='store_true', default=True, help='Run browser headless')
    parser.add_argument('--solve-cloudflare', action='store_true', help='Attempt to solve Cloudflare challenges')
    parser.add_argument('--adaptive', action='store_true', help='Use adaptive mode (relocate elements)')
    parser.add_argument('--getall', action='store_true', help='Get all matching elements (list)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    try:
        # Choose fetcher
        if args.stealth:
            page = StealthyFetcher.fetch(
                args.url, 
                headless=args.headless,
                solve_cloudflare=args.solve_cloudflare
            )
        else:
            page = Fetcher.get(args.url)
        
        # Extract content
        if args.css:
            if args.getall:
                result = page.css(args.css, adaptive=args.adaptive).getall()
            else:
                result = page.css(args.css, adaptive=args.adaptive).get()
        elif args.xpath:
            if args.getall:
                result = page.xpath(args.xpath).getall()
            else:
                result = page.xpath(args.xpath).get()
        elif args.text:
            result = page.text
        elif args.html:
            result = page.html
        else:
            # Default: return title and first 500 chars of text
            result = {
                'url': args.url,
                'title': page.css('title::text').get() or 'No title',
                'text_preview': page.text[:500] if page.text else 'No text',
                'status': 'success'
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        # Output
        if args.json:
            output = {
                'url': args.url,
                'selector': args.css or args.xpath,
                'result': result,
                'count': len(result) if isinstance(result, list) else 1
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            if isinstance(result, list):
                for item in result:
                    print(item)
            else:
                print(result)
    
    except Exception as e:
        error = {
            'url': args.url,
            'error': str(e),
            'type': type(e).__name__
        }
        print(json.dumps(error, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
