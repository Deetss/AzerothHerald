"""
Simple test script to understand Wowhead news structure
"""

import requests
from bs4 import BeautifulSoup
import re

# Fetch the page
url = "https://www.wowhead.com/news"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("=== TESTING WOWHEAD NEWS STRUCTURE ===")
    
    # Get page text and look for the article patterns we saw in the fetch
    page_text = soup.get_text()
    
    # Based on the webpage fetch, we saw patterns like:
    # "Sylvanas Windrunner's Return in Midnight Teased in Developer Interview Posted 15 hr 45 min ago by Portergauge"
    
    # Find these patterns
    article_patterns = [
        r'([A-Z][^.]*(?:Sylvanas|Midnight|Mythic|World First|Season|Patch|Hotfix|Alpha|Beta|PTR)[^.]*?)(?:\s+Posted\s+|\s+LIVE\s+)',
        r'(World First[^.]{10,80})',
        r'(Midnight[^.]{10,80})',
        r'(Mythic[^.]{10,80})',
        r'(Season[^.]{10,80})',
        r'(Patch[^.]{10,80})',
        r'(Hotfix[^.]{10,80})',
    ]
    
    found_articles = []
    
    for pattern in article_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                title = match[0].strip()
            else:
                title = match.strip()
            
            # Clean up the title
            title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with single space
            title = title.replace('LIVE', '').strip()
            
            if len(title) >= 20 and title not in found_articles:
                found_articles.append(title)
                
    print(f"Found {len(found_articles)} potential articles:")
    for i, title in enumerate(found_articles[:10]):
        print(f"{i+1}. {title}")
    
    # Also try to find any script tags with data
    scripts = soup.find_all('script')
    json_scripts = 0
    for script in scripts:
        if script.string and len(script.string) > 500:
            if 'news' in script.string.lower() or 'article' in script.string.lower():
                json_scripts += 1
    
    print(f"\nFound {json_scripts} script tags that might contain article data")
    
except Exception as e:
    print(f"Error: {e}")
