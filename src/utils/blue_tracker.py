"""
Blue Tracker scraping utility for Wowhead Blue Tracker posts.
Monitors for new official Blizzard posts and announcements.
"""

import os
import json
import requests
import urllib.parse
from datetime import datetime, timezone
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class BlueTrackerScraper:
    def __init__(self, region_filter='us'):
        self.url = "https://www.wowhead.com/blue-tracker"
        self.cache_file = "blue_tracker_cache.json"
        self.region_filter = region_filter.lower() if region_filter else None  # Default to US region
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def load_cache(self) -> Dict:
        """Load the cache of previously seen posts."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
        return {"last_check": None, "seen_posts": []}
    
    def save_cache(self, cache_data: Dict):
        """Save the cache of seen posts."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_blue_tracker_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the blue tracker page."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching blue tracker page: {e}")
            return None
    
    def parse_posts(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse blue tracker posts from the page."""
        posts = []
        
        try:
            # Look for script tags containing the blue tracker data
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'entries' in script.string and len(script.string) > 1000:
                    content = script.string.strip()
                    
                    # Try to extract JSON data
                    if content.startswith('{') and '"entries"' in content:
                        try:
                            import json
                            import re
                            
                            # Find the JSON object containing entries
                            json_match = re.search(r'\{.*"entries".*\}', content, re.DOTALL)
                            if json_match:
                                json_str = json_match.group(0)
                                data = json.loads(json_str)
                                
                                if 'entries' in data and isinstance(data['entries'], list):
                                    for entry in data['entries']:
                                        post_data = self.extract_post_from_json(entry)
                                        if post_data and self.is_relevant_post(post_data):
                                            posts.append(post_data)
                                    break  # Found the data, no need to continue
                                    
                        except (json.JSONDecodeError, Exception) as e:
                            print(f"Error parsing JSON data: {e}")
                            continue
                            
        except Exception as e:
            print(f"Error parsing posts: {e}")
            
        # If JSON extraction failed or returned nothing, try DOM-based scraping as a fallback
        if not posts and soup:
            try:
                anchors = soup.find_all('a', href=True)
                seen = set()
                for a in anchors:
                    href = a['href']
                    # Focus on links that likely point to blue tracker posts or Wowhead news
                    if 'blue-tracker' not in href and '/news/' not in href and 'blue-tracker/topic' not in href:
                        continue

                    title = a.get_text(strip=True)
                    if not title or len(title) < 3:
                        # try title attribute
                        title = a.get('title', '').strip()
                        if not title or len(title) < 3:
                            continue

                    # Try to find a snippet or body nearby
                    parent = a.find_parent()
                    snippet = ''
                    if parent:
                        p = parent.find('p')
                        if p:
                            snippet = p.get_text(strip=True)

                    # Try to find time/author
                    time_posted = ''
                    author = ''
                    if parent:
                        time_el = parent.find('time') or parent.find(class_=lambda c: c and 'time' in c)
                        if time_el:
                            time_posted = time_el.get('datetime') if time_el.has_attr('datetime') else time_el.get_text(strip=True)
                        author_el = parent.find(class_=lambda c: c and 'author' in c)
                        if author_el:
                            author = author_el.get_text(strip=True)

                    # Find an image in the parent or nearby elements
                    image_url = None
                    if parent:
                        img_tag = parent.find('img')
                        if img_tag and img_tag.get('src'):
                            candidate = img_tag.get('src')
                            candidate = self._normalize_image_url(candidate)
                            if self._is_valid_post_image(candidate):
                                image_url = candidate

                    if not image_url:
                        prev_img = a.find_previous('img')
                        next_img = a.find_next('img')
                        for img_tag in (prev_img, next_img):
                            if img_tag and img_tag.get('src'):
                                candidate = self._normalize_image_url(img_tag.get('src'))
                                if self._is_valid_post_image(candidate):
                                    image_url = candidate
                                    break

                    # Normalize href to absolute URL
                    if href.startswith('/'):
                        post_url = f"https://www.wowhead.com{href}"
                    elif href.startswith('http'):
                        post_url = href
                    else:
                        post_url = urllib.parse.urljoin(self.url, href)

                    post = {
                        'title': title,
                        'author': author or 'Unknown',
                        'time_posted': time_posted or '',
                        'url': post_url,
                        'content_preview': snippet,
                        'scraped_at': datetime.now(timezone.utc).isoformat(),
                        'post_id': '',
                        'region': '',
                        'image_url': image_url
                    }

                    if self.is_relevant_post(post):
                        key = f"{post_url}|{title}"
                        if key not in seen:
                            posts.append(post)
                            seen.add(key)
                    if len(posts) >= 10:
                        break
            except Exception as e:
                print(f"Error in DOM fallback scraping: {e}")

        return posts
    
    def extract_post_from_json(self, entry: Dict) -> Optional[Dict]:
        """Extract post data from a JSON entry."""
        try:
            title = entry.get('title', '')
            author = entry.get('author', entry.get('userName', 'Unknown'))
            posted = entry.get('posted', entry.get('timestamp', ''))
            post_id = entry.get('id', '')
            body = entry.get('body', '')
            region = entry.get('region', '').lower()
            
            # Extract image/banner URL if available
            image_url = None
            # Check for various image fields in the JSON entry
            if 'image' in entry and entry['image']:
                image_url = entry['image']
            elif 'banner' in entry and entry['banner']:
                image_url = entry['banner']
            elif 'thumbnail' in entry and entry['thumbnail']:
                image_url = entry['thumbnail']
            elif 'img' in entry and entry['img']:
                image_url = entry['img']
            
            # If image_url is relative, make it absolute
            if image_url:
                if image_url.startswith('/'):
                    image_url = f"https://www.wowhead.com{image_url}"
                elif image_url.startswith('//'):
                    image_url = f"https:{image_url}"
            
            # Try to extract image from body content if no direct image found
            if not image_url and body:
                image_url = self._extract_image_from_content(body)
            
            # For news articles, try to fetch the banner image from the actual news page
            if not image_url and entry.get('news') and entry.get('url'):
                image_url = self._fetch_news_banner_image(entry['url'])
            
            # Filter by region if specified
            if self.region_filter and region and region != self.region_filter:
                return None  # Skip posts from other regions
            
            # Convert timestamp if needed
            time_posted = posted
            if posted:
                try:
                    from datetime import datetime
                    # Try to parse the timestamp and make it more readable
                    if ' ' in posted:  # Format like "2025-08-23 12:51:17"
                        dt = datetime.strptime(posted, "%Y-%m-%d %H:%M:%S")
                        time_posted = dt.strftime("%B %d, %Y at %I:%M %p")
                except:
                    time_posted = posted
            
            # Build URL - prioritize actual URLs from the data
            post_url = None
            
            # First, check if there's a direct URL in the entry
            if 'url' in entry and entry['url']:
                url_candidate = entry['url']
                # If it's a relative URL, make it absolute
                if url_candidate.startswith('/'):
                    post_url = f"https://www.wowhead.com{url_candidate}"
                else:
                    post_url = url_candidate
            elif 'link' in entry and entry['link']:
                url_candidate = entry['link']
                if url_candidate.startswith('/'):
                    post_url = f"https://www.wowhead.com{url_candidate}"
                else:
                    post_url = url_candidate
            elif 'source_url' in entry and entry['source_url']:
                url_candidate = entry['source_url']
                if url_candidate.startswith('/'):
                    post_url = f"https://www.wowhead.com{url_candidate}"
                else:
                    post_url = url_candidate
            elif post_id:
                # Try different URL patterns based on the source
                # Check if this looks like a Wowhead news ID (usually longer numbers)
                if len(str(post_id)) > 6:
                    # This might be a Wowhead news article
                    post_url = f"https://www.wowhead.com/news/{post_id}"
                else:
                    # For shorter IDs, try forum structure but make it more robust
                    # Some might be EU forums, some US, some from different game forums
                    post_url = f"https://www.wowhead.com/blue-tracker/topic/{post_id}"
            
            # If we still don't have a URL, create a search link to Wowhead blue tracker
            if not post_url and title:
                # Create a search URL that will help users find the post
                search_title = urllib.parse.quote(title[:50])  # Limit search term length
                post_url = f"https://www.wowhead.com/blue-tracker?search={search_title}"
            
            if title and len(title) > 5:
                return {
                    'title': title,
                    'author': author,
                    'time_posted': time_posted,
                    'url': post_url,
                    'content_preview': body[:200] + "..." if len(body) > 200 else body,
                    'scraped_at': datetime.now(timezone.utc).isoformat(),
                    'post_id': str(post_id),
                    'region': region,
                    'image_url': image_url  # Add image URL to the returned data
                }
                
        except Exception as e:
            print(f"Error extracting post from JSON: {e}")
            
        return None

    def _extract_image_from_content(self, content: str) -> Optional[str]:
        """Extract image URLs from post content (HTML or text)."""
        try:
            import re
            
            # Look for img tags in HTML content
            img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
            img_matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            for img_src in img_matches:
                if self._is_valid_post_image(img_src):
                    return self._normalize_image_url(img_src)
            
            # Look for direct image URLs in text
            url_pattern = r'https?://[^\s<>"]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s<>"]*)?'
            url_matches = re.findall(url_pattern, content, re.IGNORECASE)
            
            for img_url in url_matches:
                if self._is_valid_post_image(img_url):
                    return img_url
            
            return None
        except Exception as e:
            print(f"Error extracting image from content: {e}")
            return None

    def _is_valid_post_image(self, src: str) -> bool:
        """Check if an image src is likely to be a valid post image."""
        if not src or len(src) < 10:
            return False
        
        # Skip obviously non-post images
        skip_patterns = [
            'avatar', 'icon-small', 'emoji', 'smiley', 'button',
            'nav', 'menu', 'logo-small', 'signature',
            'share-icon', 'facebook', 'twitter', 'social',
            'logo.png', 'favicon', 'generic', 'placeholder'
        ]
        
        src_lower = src.lower()
        if any(pattern in src_lower for pattern in skip_patterns):
            return False
        
        # Accept images from trusted domains or with good patterns
        trusted_domains = ['blizzard.com', 'battle.net', 'wowhead.com', 'wow.zamimg.com']
        good_patterns = ['screenshot', 'image', 'content', 'post', 'news', 'announcement', 'banner', 'header']
        
        return (any(domain in src_lower for domain in trusted_domains) and
                any(pattern in src_lower for pattern in good_patterns) and
                # Accept if it's a reasonable sized image URL
                len(src) > 30)

    def _normalize_image_url(self, url: str) -> str:
        """Normalize an image URL to be absolute and properly formatted."""
        if url.startswith('//'):
            return f"https:{url}"
        elif url.startswith('/'):
            return f"https://www.wowhead.com{url}"
        elif not url.startswith('http'):
            return f"https://www.wowhead.com/{url}"
        return url
    
    def _fetch_news_banner_image(self, news_url: str) -> Optional[str]:
        """Fetch the banner image from a Wowhead news article page."""
        try:
            import requests
            
            # Convert relative URL to absolute
            if news_url.startswith('/'):
                full_url = f"https://www.wowhead.com{news_url}"
            else:
                full_url = news_url
            
            # Fetch the news page
            response = requests.get(full_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse the page
            news_soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for common news banner patterns
            banner_selectors = [
                'img.news-banner',
                'img.article-banner', 
                '.news-header img',
                '.article-header img',
                'meta[property="og:image"]',
                'meta[name="twitter:image"]'
            ]
            
            for selector in banner_selectors:
                if selector.startswith('meta'):
                    meta_tag = news_soup.find('meta', attrs={'property' if 'property' in selector else 'name': selector.split('"')[1]})
                    if meta_tag and meta_tag.get('content'):
                        image_url = meta_tag['content']
                        if self._is_valid_post_image(image_url):
                            return self._normalize_image_url(image_url)
                else:
                    img_tag = news_soup.select_one(selector)
                    if img_tag and img_tag.get('src'):
                        image_url = img_tag['src']
                        if self._is_valid_post_image(image_url):
                            return self._normalize_image_url(image_url)
            
            # Fallback: look for any large image in the content area
            content_area = news_soup.find('div', class_=['news-content', 'article-content', 'content'])
            if content_area:
                images = content_area.find_all('img')
                for img in images:
                    if img.get('src') and self._is_valid_post_image(img['src']):
                        return self._normalize_image_url(img['src'])
            
            return None
            
        except Exception as e:
            print(f"Error fetching news banner image from {news_url}: {e}")
            return None
    
    def is_relevant_post(self, post_data: Dict) -> bool:
        """Determine if a post is relevant for notifications."""
        if not post_data or not post_data.get('title'):
            return False
            
        title = post_data['title'].lower()
        author = post_data.get('author', '').lower()
        
        # Filter for official Blizzard posts and Community Managers
        official_authors = [
            'blizzard entertainment',
            'kaivax',
            'linxy', 
            'nethaera',
            'blizzard',
            'community manager'
        ]
        
        is_official = any(auth in author for auth in official_authors)
        
        # Filter for important content types
        important_keywords = [
            'hotfix', 'patch', 'update', 'maintenance', 'downtime',
            'class tuning', 'dungeon tuning', 'raid', 'mythic+', 'mythic plus',
            'developer', 'announcement', 'notes', 'bug fix', 'bugfix',
            'weekly', 'season', 'expansion', 'ptr', 'public test',
            'balance', 'nerf', 'buff', 'adjustment', 'incoming',
            'development notes', 'known issues', 'preview'
        ]
        
        has_important_content = any(keyword in title for keyword in important_keywords)
        
        # Exclude less important posts
        exclude_keywords = [
            'bug report', 'suggestions', 'feedback',
            'ui addon', 'technical support', 'customer service',
            'account', 'billing', 'refund'
        ]
        
        has_excluded_content = any(keyword in title for keyword in exclude_keywords)
        
        # For Blizzard Entertainment, be less strict about keywords
        if 'blizzard entertainment' in author:
            # Include all Blizzard Entertainment posts except excluded ones
            return not has_excluded_content
        
        # For Community Managers, require important keywords
        return is_official and has_important_content and not has_excluded_content
    
    def get_new_posts(self) -> List[Dict]:
        """Get new posts since last check."""
        cache = self.load_cache()
        seen_posts = set(cache.get('seen_posts', []))
        is_first_run = len(seen_posts) == 0 and cache.get('last_check') is None
        
        soup = self.fetch_blue_tracker_page()
        if not soup:
            return []
            
        all_posts = self.parse_posts(soup)
        new_posts = []
        
        for post in all_posts:
            # Create a unique identifier for the post using post_id if available
            post_id = post.get('post_id', '')
            if post_id:
                unique_id = f"id_{post_id}"
            else:
                # Fallback to title-author-time for posts without IDs
                unique_id = f"{post['title']}_{post['author']}_{post.get('time_posted', '')}"
            
            if unique_id not in seen_posts:
                new_posts.append(post)
                seen_posts.add(unique_id)
        
        # On first run, limit to the most recent 3 posts to avoid spam
        if is_first_run and new_posts:
            print(f"First run detected - returning {min(3, len(new_posts))} most recent posts")
            new_posts = new_posts[:3]
            # Still mark all posts as seen to avoid future duplicates
            # (seen_posts already contains all post IDs from above loop)
        
        # Update cache
        cache['seen_posts'] = list(seen_posts)
        cache['last_check'] = datetime.now(timezone.utc).isoformat()
        self.save_cache(cache)
        
        return new_posts
    
    def format_post_for_discord(self, post: Dict) -> Dict:
        """Format a post for Discord embed."""
        title = post['title'][:256]  # Discord title limit
        author = post.get('author', 'Unknown')
        time_posted = post.get('time_posted', 'Unknown')
        url = post.get('url')
        
        description_parts = []
        if author != 'Unknown':
            description_parts.append(f"**Author:** {author}")
        if time_posted != 'Unknown':
            description_parts.append(f"**Posted:** {time_posted}")
        
        # Add content preview if available
        preview = post.get('content_preview', '')
        if preview and len(preview) > 50:
            description_parts.append(f"\n{preview}")
        
        # Add note about URL if it's a search link
        if url and 'search=' in url:
            description_parts.append(f"\n*Click title to search for this post on Wowhead Blue Tracker*")
        
        description = "\n".join(description_parts)[:4096]  # Discord description limit
        
        embed_data = {
            'title': title,
            'description': description,
            'color': 0x00b4d8,  # Blue color for Blizzard posts
            'timestamp': post.get('scraped_at'),
            'footer': {'text': 'Wowhead Blue Tracker - Click title for source'}
        }
        
        if url:
                embed_data['url'] = url

        # Add image if available
        image_url = post.get('image_url')
        if image_url:
                embed_data['image'] = {'url': image_url}
            
        return embed_data
    
    def get_reset_relevant_posts(self, days_back: int = 7) -> List[Dict]:
        """Get recent posts that are relevant to weekly reset activities."""
        from datetime import datetime, timedelta
        
        # Get all cached posts first
        cache = self.load_cache()
        
        # Also fetch fresh posts to make sure we have the latest
        soup = self.fetch_blue_tracker_page()
        if soup:
            fresh_posts = self.parse_posts(soup)
        else:
            fresh_posts = []
        
        # Filter posts from the last X days that are reset-relevant
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        relevant_posts = []
        
        for post in fresh_posts:
            try:
                # Check if post is recent enough
                scraped_time = datetime.fromisoformat(post.get('scraped_at', '').replace('Z', '+00:00'))
                if scraped_time < cutoff_date:
                    continue
                
                if self.is_reset_relevant(post):
                    relevant_posts.append(post)
            except Exception as e:
                print(f"Error processing post for reset relevance: {e}")
                continue
        
        return relevant_posts
    
    def is_reset_relevant(self, post: Dict) -> bool:
        """Check if a post contains information relevant to weekly reset activities."""
        if not post or not post.get('title'):
            return False
        
        title = post['title'].lower()
        content = post.get('content_preview', '').lower()
        combined_text = f"{title} {content}"
        
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
            
            # Profession related (since it's in weekly checklist)
            'profession', 'crafting', 'knowledge point',
            
            # PvP (Great Vault)
            'pvp season', 'rated pvp', 'arena', 'conquest', 'honor'
        ]
        
        # Timing keywords that suggest something is happening soon
        timing_keywords = [
            'this week', 'next week', 'coming week', 'upcoming',
            'starting', 'ending', 'begins', 'concludes',
            'tuesday', 'wednesday', 'thursday', 'friday',
            'tomorrow', 'today', 'soon', 'incoming'
        ]
        
        # Check for reset-relevant content
        has_reset_content = any(keyword in combined_text for keyword in reset_keywords)
        has_timing_info = any(keyword in combined_text for keyword in timing_keywords)
        
        # Also prioritize official announcements and developer posts
        is_high_priority = any(term in combined_text for term in [
            'developer', 'announcement', 'upcoming changes',
            'ptr', 'public test', 'preview', 'known issues'
        ])
        
        return has_reset_content or (has_timing_info and is_high_priority)
    
    def summarize_reset_info(self, posts: List[Dict]) -> Dict:
        """Summarize reset-relevant information from posts."""
        if not posts:
            return {}
        
        summary = {
            'this_week': [],
            'next_week': [],
            'general': []
        }
        
        for post in posts:
            title = post['title']
            content = post.get('content_preview', '').lower()
            combined = f"{title.lower()} {content}"
            
            # Categorize by timing
            if any(term in combined for term in ['this week', 'starting', 'begins', 'today', 'tomorrow']):
                summary['this_week'].append({
                    'title': title,
                    'url': post.get('url'),
                    'preview': content[:100] + "..." if len(content) > 100 else content
                })
            elif any(term in combined for term in ['next week', 'upcoming', 'coming', 'soon']):
                summary['next_week'].append({
                    'title': title,
                    'url': post.get('url'),
                    'preview': content[:100] + "..." if len(content) > 100 else content
                })
            else:
                summary['general'].append({
                    'title': title,
                    'url': post.get('url'),
                    'preview': content[:100] + "..." if len(content) > 100 else content
                })
        
        return summary
