#!/usr/bin/env python3
"""
Extract Blue Tracker data from JavaScript variables on the page.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
import json
import re

def extract_blue_tracker_data():
    """Extract blue tracker data from JavaScript on the page."""
    print("🔍 Extracting Blue Tracker JavaScript Data")
    print("=" * 60)
    
    url = "https://www.wowhead.com/blue-tracker"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✅ Successfully fetched page (Status: {response.status_code})")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for all script tags
        scripts = soup.find_all('script')
        print(f"📜 Found {len(scripts)} script tags")
        
        for i, script in enumerate(scripts):
            if script.string:
                content = script.string.strip()
                
                # Look for various data patterns
                if 'entries' in content.lower() and len(content) > 100:
                    print(f"\n📋 Script {i} contains 'entries' (length: {len(content)}):")
                    
                    # Try to find JSON-like data
                    if content.startswith('{') or '"entries"' in content:
                        print("   JSON-like content found!")
                        print(f"   First 300 chars: {content[:300]}...")
                        
                        # Try to extract JSON
                        try:
                            # Look for JSON in various formats
                            json_match = re.search(r'\{.*"entries".*\}', content, re.DOTALL)
                            if json_match:
                                json_str = json_match.group(0)
                                data = json.loads(json_str)
                                if 'entries' in data and isinstance(data['entries'], list):
                                    print(f"   ✅ Found {len(data['entries'])} entries!")
                                    
                                    # Show sample entries
                                    for j, entry in enumerate(data['entries'][:3]):
                                        print(f"   Entry {j+1}:")
                                        print(f"     Title: {entry.get('title', 'No title')}")
                                        print(f"     ID: {entry.get('id', 'No ID')}")
                                        if 'userName' in entry:
                                            print(f"     Author: {entry['userName']}")
                                        print()
                                    
                                    return data
                        except json.JSONDecodeError:
                            print("   ❌ Could not parse as JSON")
                    
                    elif content.startswith('var ') and '=' in content:
                        print("   Variable assignment found!")
                        print(f"   First 300 chars: {content[:300]}...")
        
        print("\n❌ No blue tracker data found in JavaScript")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = extract_blue_tracker_data()
    if result:
        print(f"\n🎉 Successfully extracted data with {len(result.get('entries', []))} entries!")
    else:
        print("\n😞 Could not extract blue tracker data")
