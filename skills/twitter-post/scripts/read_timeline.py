#!/home/deck/.openclaw/workspace/skills/twitter-post/venv/bin/python3
"""
Read @HelvetiVault timeline to understand existing identity
"""

import sys
import json
import tweepy
from pathlib import Path

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

def read_timeline(count=20):
    """Read recent tweets from @HelvetiVault"""
    
    # Load credentials
    creds, error = load_credentials()
    if error:
        return {"error": "CREDENTIALS_ERROR", "message": error}
    
    try:
        # Authenticate with Twitter API v1.1
        auth = tweepy.OAuth1UserHandler(
            creds["apiKey"],
            creds["apiSecret"],
            creds["accessToken"],
            creds["accessTokenSecret"]
        )
        
        api = tweepy.API(auth)
        
        # Get my own tweets
        tweets = api.user_timeline(count=count, tweet_mode="extended")
        
        timeline = []
        for tweet in tweets:
            timeline.append({
                "id": str(tweet.id),
                "text": tweet.full_text,
                "created_at": tweet.created_at.isoformat(),
                "retweets": tweet.retweet_count,
                "likes": tweet.favorite_count,
                "url": f"https://twitter.com/HelvetiVault/status/{tweet.id}"
            })
        
        return {
            "status": "success",
            "account": "@HelvetiVault",
            "tweets_count": len(timeline),
            "tweets": timeline
        }
        
    except Exception as e:
        return {
            "error": "API_ERROR",
            "message": f"Failed to read timeline: {str(e)}"
        }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    result = read_timeline(count)
    print(json.dumps(result, ensure_ascii=False, indent=2))
