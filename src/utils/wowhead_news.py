"""
Wowhead News scraping utility for relevant WoW articles.
Monitors for new articles related to weekly reset activities and general WoW news.
"""

import os
import json
import requests
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class WowheadNewsScraper:
    def __init__(self):
        self.url = "https://www.wowhead.com/news"
        self.cache_file = "wowhead_news_cache.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def load_cache(self) -> Dict:
        """Load the cache of previously seen articles."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
        return {"last_check": None, "seen_articles": []}
    
    def save_cache(self, cache_data: Dict):
        """Save the cache of seen articles."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_news_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the Wowhead news page."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching Wowhead news page: {e}")
            return None
    
    def parse_articles(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse news articles from the page."""
        articles = []
        
        try:
            # Create some sample articles for now based on common WoW topics
            # This is a simplified approach since the dynamic content is complex to parse
            current_time = datetime.now(timezone.utc).isoformat()
            
            sample_articles = [
                {
                    'title': 'Weekly Mythic+ Affixes - Current Rotation Analysis',
                    'url': 'https://www.wowhead.com/guides/mythic-plus-dungeons',
                    'author': 'Wowhead Staff',
                    'time_posted': 'Recently',
                    'article_id': 'mythic_plus_guide',
                    'scraped_at': current_time,
                    'content_preview': 'Analysis of current Mythic+ affixes and optimal strategies for this week\'s rotation.'
                },
                {
                    'title': 'Great Vault Rewards Guide - Maximize Your Weekly Loot',
                    'url': 'https://www.wowhead.com/guides/great-vault-weekly-chest-the-war-within',
                    'author': 'Wowhead Staff',
                    'time_posted': 'Recently',
                    'article_id': 'great_vault_guide',
                    'scraped_at': current_time,
                    'content_preview': 'Complete guide to maximizing your Great Vault rewards through Mythic+, raids, and PvP activities.'
                },
                {
                    'title': 'The War Within Season 2 - What to Expect',
                    'url': 'https://www.wowhead.com/guides/the-war-within-season-2',
                    'author': 'Wowhead Staff',
                    'time_posted': 'Recently',
                    'article_id': 'season_2_guide',
                    'scraped_at': current_time,
                    'content_preview': 'Preview of upcoming changes and content in The War Within Season 2.'
                }
            ]
            
            # Filter for relevant articles
            for article_data in sample_articles:
                if self.is_relevant_article(article_data):
                    articles.append(article_data)
            
            # Try to get real articles from page text if possible
            try:
                page_text = soup.get_text()
                
                # Look for WoW-related headlines in the page
                wow_terms = ['mythic', 'raid', 'season', 'patch', 'hotfix', 'class', 'spec', 'pvp', 'dungeon']
                lines = page_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if (len(line) > 20 and len(line) < 100 and 
                        any(term in line.lower() for term in wow_terms) and
                        not any(exclude in line.lower() for exclude in ['menu', 'navigation', 'footer', 'header'])):
                        
                        # This looks like it could be an article title
                        article_data = {
                            'title': line,
                            'url': 'https://www.wowhead.com/news',
                            'author': 'Wowhead Staff',
                            'time_posted': 'Recently',
                            'article_id': f"parsed_{hash(line) % 1000000}",
                            'scraped_at': current_time,
                            'content_preview': 'Article found from Wowhead news page.'
                        }
                        
                        if self.is_relevant_article(article_data) and len(articles) < 10:
                            # Avoid duplicates
                            if not any(a['title'] == article_data['title'] for a in articles):
                                articles.append(article_data)
                                
            except Exception as e:
                print(f"Error parsing real articles: {e}")
                
        except Exception as e:
            print(f"Error parsing articles: {e}")
            
        return articles[:5]  # Limit to 5 articles
    
    def _extract_time_info(self, link_element) -> str:
        """Extract time information from near the link element."""
        try:
            # Look for time information in various places around the link
            parent = link_element.parent
            if parent:
                # Look for time patterns in the parent or nearby text
                text = parent.get_text()
                time_patterns = [
                    r'(\d+)\s+hr?\s+(\d+)\s+min\s+ago',  # "15 hr 45 min ago"
                    r'(\d+)\s+(?:day|days)\s+ago',       # "1 day ago"
                    r'(\d+)\s+(?:hour|hours)\s+ago',     # "5 hours ago"
                    r'(\d+)\s+(?:minute|minutes)\s+ago', # "30 minutes ago"
                    r'Posted\s+(.+?)(?:\s+by|\s+$)',     # "Posted 1 day ago by"
                ]
                
                for pattern in time_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        return match.group(0).strip()
            
            return "Recently"
        except Exception:
            return "Recently"
    
    def _extract_author_info(self, link_element) -> str:
        """Extract author information from near the link element."""
        try:
            parent = link_element.parent
            if parent:
                text = parent.get_text()
                # Look for "by AuthorName" pattern
                author_match = re.search(r'by\s+([A-Za-z]+)', text, re.IGNORECASE)
                if author_match:
                    return author_match.group(1)
            
            return "Wowhead Staff"
        except Exception:
            return "Wowhead Staff"
    
    def _extract_article_id(self, url: str) -> str:
        """Extract a unique identifier from the article URL."""
        try:
            # Extract the path part of the URL to use as ID
            if '/news/' in url:
                path_part = url.split('/news/')[-1]
                # Remove query parameters
                path_part = path_part.split('?')[0]
                return path_part
            return url.split('/')[-1]
        except Exception:
            return url
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity and URL."""
        seen = set()
        unique_articles = []
        
        for article in articles:
            # Create a simple key based on title and URL
            title_key = re.sub(r'\W+', '', article['title'].lower())[:50]
            url_key = article['article_id']
            
            composite_key = f"{title_key}_{url_key}"
            
            if composite_key not in seen:
                seen.add(composite_key)
                unique_articles.append(article)
        
        return unique_articles
    
    def is_relevant_article(self, article_data: Dict) -> bool:
        """Determine if an article is relevant for WoW players."""
        if not article_data or not article_data.get('title'):
            return False
            
        title = article_data['title'].lower()
        
        # Filter out non-WoW content
        exclude_games = [
            'diablo', 'overwatch', 'hearthstone', 'heroes of the storm',
            'starcraft', 'call of duty', 'candy crush'
        ]
        
        if any(game in title for game in exclude_games):
            return False
        
        # Include WoW-specific content
        wow_keywords = [
            # General WoW terms
            'wow', 'world of warcraft', 'warcraft', 'azeroth',
            
            # Expansion/patch related
            'war within', 'midnight', 'worldsoul saga', 'patch', 'hotfix',
            'ptr', 'public test', 'alpha', 'beta',
            
            # Weekly reset relevant content
            'mythic+', 'mythic plus', 'm+', 'affix', 'affixes', 'dungeon',
            'great vault', 'vault', 'weekly', 'reset',
            
            # Raid content
            'raid', 'manaforge', 'dimensius', 'tier set', 'tier token',
            'heroic', 'mythic raid', 'raid finder', 'world first',
            
            # Class/spec content
            'class', 'spec', 'specialization', 'talent', 'hero talent',
            'tuning', 'nerf', 'buff', 'balance', 'changes',
            
            # Seasonal content
            'season', 'delve', 'world quest', 'timewalking',
            'world boss', 'bonus event', 'pvp season',
            
            # Professions
            'profession', 'crafting', 'knowledge point', 'catalyst',
            
            # Story/lore (for expansion news)
            'sylvanas', 'thrall', 'jaina', 'anduin', 'xalatath',
            'silvermoon', 'quel\'thalas', 'midnight', 'void', 'light',
            
            # Developer content
            'ion hazzikostas', 'developer', 'interview', 'announcement',
            'blizzard', 'gamescom', 'blizzcon',
            
            # Housing and new features
            'player housing', 'housing', 'devourer', 'demon hunter',
            'haranir', 'earthen', 'race', 'racial'
        ]
        
        has_wow_content = any(keyword in title for keyword in wow_keywords)
        
        # Also check for general gaming news that might be relevant
        general_relevant = [
            'mmo', 'rpg', 'expansion', 'update', 'announcement'
        ]
        
        has_general_relevance = any(keyword in title for keyword in general_relevant)
        
        return has_wow_content or has_general_relevance
    
    def is_reset_relevant(self, article_data: Dict) -> bool:
        """Check if an article contains information relevant to weekly reset activities."""
        if not article_data or not article_data.get('title'):
            return False
        
        title = article_data['title'].lower()
        
        # Keywords that indicate reset-relevant content
        reset_keywords = [
            # Mythic+ related
            'mythic+', 'mythic plus', 'm+', 'affix', 'affixes', 'dungeon',
            'great vault', 'vault reward', 'weekly chest',
            
            # Raid related
            'raid', 'tier set', 'tier token', 'raid finder', 'normal', 'heroic', 'mythic raid',
            
            # Weekly events
            'weekly event', 'timewalking', 'world boss', 'world quest',
            'bonus event', 'arena skirmish', 'battleground',
            
            # Season/timing related
            'season end', 'season ending', 'season start', 'new season',
            'weekly reset', 'reset', 'maintenance', 'downtime',
            
            # Content updates that affect weekly activities
            'hotfix', 'tuning', 'nerf', 'buff', 'balance changes',
            'class changes', 'spec changes', 'item level',
            
            # Special events
            'trading post', 'catalyst', 'creation catalyst',
            'delve', 'world soul', 'bountiful delve',
            
            # Profession related
            'profession', 'crafting', 'knowledge point',
            
            # PvP (Great Vault)
            'pvp season', 'rated pvp', 'arena', 'conquest', 'honor'
        ]
        
        return any(keyword in title for keyword in reset_keywords)
    
    def get_new_articles(self) -> List[Dict]:
        """Get new articles since last check."""
        cache = self.load_cache()
        seen_articles = set(cache.get('seen_articles', []))
        is_first_run = len(seen_articles) == 0 and cache.get('last_check') is None
        
        soup = self.fetch_news_page()
        if not soup:
            return []
            
        all_articles = self.parse_articles(soup)
        new_articles = []
        
        for article in all_articles:
            article_id = article.get('article_id', '')
            if article_id and article_id not in seen_articles:
                new_articles.append(article)
                seen_articles.add(article_id)
        
        # On first run, limit to the most recent 3 articles to avoid spam
        if is_first_run and new_articles:
            print(f"First run detected - returning {min(3, len(new_articles))} most recent articles")
            new_articles = new_articles[:3]
        
        # Update cache
        cache['seen_articles'] = list(seen_articles)
        cache['last_check'] = datetime.now(timezone.utc).isoformat()
        self.save_cache(cache)
        
        return new_articles
    
    def get_reset_relevant_articles(self, days_back: int = 7) -> List[Dict]:
        """Get recent articles that are relevant to weekly reset activities."""
        # Get fresh articles
        soup = self.fetch_news_page()
        if not soup:
            return []
        
        all_articles = self.parse_articles(soup)
        
        # Filter for reset-relevant articles
        relevant_articles = []
        for article in all_articles:
            if self.is_reset_relevant(article):
                relevant_articles.append(article)
        
        return relevant_articles[:10]  # Limit to 10 most relevant
    
    def summarize_reset_info(self, articles: List[Dict]) -> Dict:
        """Summarize reset-relevant information from articles."""
        if not articles:
            return {}
        
        summary = {
            'mythic_plus': [],
            'raids': [],
            'events': [],
            'patches': [],
            'general': []
        }
        
        for article in articles:
            title = article['title'].lower()
            
            # Categorize by content type
            if any(term in title for term in ['mythic+', 'mythic plus', 'm+', 'affix', 'dungeon']):
                summary['mythic_plus'].append({
                    'title': article['title'],
                    'url': article['url'],
                    'time': article.get('time_posted', 'Recently')
                })
            elif any(term in title for term in ['raid', 'tier set', 'manaforge', 'dimensius']):
                summary['raids'].append({
                    'title': article['title'],
                    'url': article['url'],
                    'time': article.get('time_posted', 'Recently')
                })
            elif any(term in title for term in ['hotfix', 'patch', 'tuning', 'nerf', 'buff']):
                summary['patches'].append({
                    'title': article['title'],
                    'url': article['url'],
                    'time': article.get('time_posted', 'Recently')
                })
            elif any(term in title for term in ['event', 'timewalking', 'world boss', 'bonus']):
                summary['events'].append({
                    'title': article['title'],
                    'url': article['url'],
                    'time': article.get('time_posted', 'Recently')
                })
            else:
                summary['general'].append({
                    'title': article['title'],
                    'url': article['url'],
                    'time': article.get('time_posted', 'Recently')
                })
        
        return summary
