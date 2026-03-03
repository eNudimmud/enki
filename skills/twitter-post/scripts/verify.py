#!/home/deck/.openclaw/workspace/skills/twitter-post/venv/bin/python3
"""
Verify Twitter API connection and check account info
"""

import json
import tweepy
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"

def verify_connection():
    """Verify we're connected to the right account"""
    
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        
        creds = config.get("social", {}).get("twitter", {}).get("credentials", {})
        
        if not creds:
            return {"error": "CREDENTIALS_MISSING"}
        
        # Authenticate
        auth = tweepy.OAuth1UserHandler(
            creds["apiKey"],
            creds["apiSecret"],
            creds["accessToken"],
            creds["accessTokenSecret"]
        )
        
        api = tweepy.API(auth)
        
        # Verify credentials (this returns the authenticated user)
        me = api.verify_credentials()
        
        return {
            "status": "connected",
            "username": me.screen_name,
            "name": me.name,
            "id": str(me.id),
            "followers": me.followers_count,
            "following": me.friends_count,
            "tweets": me.statuses_count,
            "account_created": me.created_at.isoformat()
        }
        
    except Exception as e:
        return {
            "error": "CONNECTION_FAILED",
            "message": str(e)
        }

if __name__ == "__main__":
    result = verify_connection()
    print(json.dumps(result, ensure_ascii=False, indent=2))
