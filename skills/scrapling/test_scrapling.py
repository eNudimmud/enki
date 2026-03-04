from scrapling.fetchers import Fetcher

# Test 1: HTTP simple (no browser)
print("Test 1: HTTP Fetcher")
page = Fetcher.get('https://httpbin.org/html')
title = page.css('h1::text').get()
print(f"✓ Title: {title}")

# Test 2: Adaptive mode
print("\nTest 2: Adaptive mode")
page2 = Fetcher.get('https://quotes.toscrape.com/')
quotes = page2.css('.quote .text::text', auto_save=True)
print(f"✓ Found {len(quotes)} quotes")

print("\n✅ Basic tests passed!")
