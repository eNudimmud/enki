#!/home/deck/.openclaw/workspace/skills/twitter-post/venv/bin/python3
"""
E*NKI Twitter Posting Script (API v2)
Posts tweets to @HelvetiVault using POST /2/tweets endpoint
"""

import sys
import json
import tweepy
from pathlib import Path
from datetime import datetime

# Load credentials from openclaw.json
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"

def load_credentials():
    """Load Twitter API credentials from OpenClaw config"""
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        
        twitter_config = config.get("social", {}).get("twitter", {})
        creds = twitter_config.get("credentials", {})
        
        if not creds:
            return None, "Twitter credentials not found in openclaw.json"
        
        return creds, None
    except Exception as e:
        return None, f"Failed to load config: {str(e)}"

def post_tweet(text, media_path=None, dry_run=False):
    """Post a tweet to @HelvetiVault using API v2"""
    
    # Load credentials
    creds, error = load_credentials()
    if error:
        return {"error": "CREDENTIALS_ERROR", "message": error}
    
    # Dry run: just preview
    if dry_run:
        return {
            "status": "preview",
            "text": text,
            "length": len(text),
            "media": media_path if media_path else None,
            "message": "Dry run — tweet not posted"
        }
    
    try:
        # Create Twitter API v2 client with OAuth 1.0a
        client = tweepy.Client(
            consumer_key=creds["apiKey"],
            consumer_secret=creds["apiSecret"],
            access_token=creds["accessToken"],
            access_token_secret=creds["accessTokenSecret"]
        )
        
        # Post tweet using API v2
        if media_path:
            # TODO: Media upload requires separate API v1.1 auth
            # For now, just post text
            response = client.create_tweet(text=text)
        else:
            response = client.create_tweet(text=text)
        
        # Extract tweet data
        tweet_id = response.data['id']
        tweet_url = f"https://twitter.com/HelvetiVault/status/{tweet_id}"
        
        result = {
            "status": "success",
            "tweet_id": tweet_id,
            "url": tweet_url,
            "text": text,
            "posted_at": datetime.utcnow().isoformat() + "Z",
            "account": "@HelvetiVault"
        }
        
        return result
        
    except tweepy.errors.Forbidden as e:
        return {
            "error": "API_FORBIDDEN",
            "message": f"Twitter API forbidden: {str(e)}"
        }
    except tweepy.errors.TooManyRequests as e:
        return {
            "error": "RATE_LIMIT",
            "message": "Twitter API rate limit reached. Try again later."
        }
    except Exception as e:
        return {
            "error": "UNKNOWN_ERROR",
            "message": f"Failed to post tweet: {str(e)}"
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "USAGE_ERROR",
            "message": "Usage: post_v2.py <text> [--media <path>] [--dry-run]"
        }))
        sys.exit(1)
    
    text = sys.argv[1]
    media_path = None
    dry_run = False
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--media" and i + 1 < len(sys.argv):
            media_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1
    
    # Validate text length
    if len(text) > 280:
        print(json.dumps({
            "error": "TEXT_TOO_LONG",
            "message": f"Tweet is {len(text)} characters (max 280)",
            "length": len(text)
        }))
        sys.exit(1)
    
    # Post tweet
    result = post_tweet(text, media_path, dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
