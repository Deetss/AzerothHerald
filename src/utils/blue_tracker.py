"""
Wowhead Blue Tracker RSS utility.

Uses Wowhead's public Blue Tracker RSS feed
(https://www.wowhead.com/blue-tracker?rss) instead of scraping the HTML page,
which sits behind Cloudflare bot protection.
"""

import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class BlueTrackerScraper:
    def __init__(self, region_filter: Optional[str] = "us") -> None:
        self.url = "https://www.wowhead.com/blue-tracker?rss"
        self.cache_file = "blue_tracker_cache.json"
        self.region_filter = region_filter.lower() if region_filter else None
        self.headers = {
            "User-Agent": "AzerothHerald/1.0 (+https://github.com/Deetss/AzerothHerald)",
            "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
        }

    def load_cache(self) -> Dict:
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, encoding="utf-8") as f:
                    return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Error loading cache: %s", e)
        return {"last_check": None, "seen_posts": []}

    def save_cache(self, cache_data: Dict) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.warning("Error saving cache: %s", e)

    def fetch_blue_tracker_page(self) -> Optional[List[ET.Element]]:
        """Fetch the Blue Tracker RSS feed and return its <item> elements."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            return root.findall(".//item")
        except (requests.RequestException, ET.ParseError) as e:
            logger.error("Error fetching blue tracker feed: %s", e)
            return None

    def parse_posts(self, items: Optional[List[ET.Element]]) -> List[Dict]:
        """Normalize RSS <item> elements into post dicts (filters by region only)."""
        if not items:
            return []

        posts: List[Dict] = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for item in items[:50]:
            try:
                title = _text(item, "title")
                link = _text(item, "link")
                if not title or not link:
                    continue

                region = _extract_region(link)
                if self.region_filter and region and region != self.region_filter:
                    continue

                description = _text(item, "description")
                pub_date_raw = _text(item, "pubDate")
                guid = _text(item, "guid") or link
                post_id = _extract_post_id(guid, link)
                pub_dt = _parse_pubdate(pub_date_raw)

                posts.append({
                    "title": title,
                    "author": "Blizzard Entertainment",
                    "time_posted": _format_pubdate(pub_dt, pub_date_raw),
                    "posted_at": pub_dt.isoformat() if pub_dt else "",
                    "url": link,
                    "content_preview": _clean_description(description),
                    "scraped_at": now_iso,
                    "post_id": post_id,
                    "region": region,
                    "image_url": _first_img_src(description),
                })
            except Exception as e:  # noqa: BLE001 - keep loop alive on bad item
                logger.warning("Error parsing blue tracker item: %s", e)
                continue

        return posts

    def is_relevant_post(self, post_data: Dict) -> bool:
        """All Blue Tracker RSS items are official Blizzard posts; only filter noise."""
        if not post_data or not post_data.get("title"):
            return False

        title = post_data["title"].lower()
        exclude_keywords = [
            "bug report", "suggestions", "feedback",
            "ui addon", "technical support", "customer service",
            "account", "billing", "refund",
        ]
        return not any(k in title for k in exclude_keywords)

    def get_new_posts(self) -> List[Dict]:
        cache = self.load_cache()
        seen_posts = set(cache.get("seen_posts", []))
        is_first_run = len(seen_posts) == 0 and cache.get("last_check") is None

        items = self.fetch_blue_tracker_page()
        if items is None:
            return []

        all_posts = [p for p in self.parse_posts(items) if self.is_relevant_post(p)]
        new_posts: List[Dict] = []
        for post in all_posts:
            unique_id = f"id_{post['post_id']}" if post.get("post_id") else (
                f"{post['title']}_{post['author']}_{post.get('time_posted', '')}"
            )
            if unique_id not in seen_posts:
                new_posts.append(post)
                seen_posts.add(unique_id)

        if is_first_run and new_posts:
            logger.info("First run detected - returning %d most recent posts", min(3, len(new_posts)))
            new_posts = new_posts[:3]

        cache["seen_posts"] = list(seen_posts)
        cache["last_check"] = datetime.now(timezone.utc).isoformat()
        self.save_cache(cache)

        return new_posts

    def format_post_for_discord(self, post: Dict) -> Dict:
        title = post["title"][:256]
        author = post.get("author", "Unknown")
        time_posted = post.get("time_posted", "Unknown")
        url = post.get("url")

        description_parts = []
        if author != "Unknown":
            description_parts.append(f"**Author:** {author}")
        if time_posted != "Unknown":
            description_parts.append(f"**Posted:** {time_posted}")
        preview = post.get("content_preview", "")
        if preview and len(preview) > 50:
            description_parts.append(f"\n{preview}")

        description = "\n".join(description_parts)[:4096]

        embed_data: Dict = {
            "title": title,
            "description": description,
            "color": 0x00B4D8,
            "timestamp": post.get("scraped_at"),
            "footer": {"text": "Wowhead Blue Tracker - Click title for source"},
        }
        if url:
            embed_data["url"] = url
        image_url = post.get("image_url")
        if image_url:
            embed_data["image"] = {"url": image_url}
        return embed_data

    def get_reset_relevant_posts(self, days_back: int = 7) -> List[Dict]:
        items = self.fetch_blue_tracker_page()
        if items is None:
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
        relevant: List[Dict] = []
        for post in self.parse_posts(items):
            if not self.is_relevant_post(post):
                continue
            posted_at = post.get("posted_at")
            if posted_at:
                try:
                    if datetime.fromisoformat(posted_at) < cutoff:
                        continue
                except ValueError:
                    pass
            if self.is_reset_relevant(post):
                relevant.append(post)
        return relevant

    def is_reset_relevant(self, post: Dict) -> bool:
        if not post or not post.get("title"):
            return False

        title = post["title"].lower()
        content = post.get("content_preview", "").lower()
        combined = f"{title} {content}"

        reset_keywords = [
            "mythic+", "mythic plus", "m+", "affix", "affixes", "dungeon",
            "great vault", "vault reward", "weekly chest",
            "raid", "tier set", "tier token", "raid finder", "normal", "heroic", "mythic raid",
            "weekly event", "timewalking", "world boss", "world quest",
            "bonus event", "arena skirmish", "battleground",
            "season end", "season ending", "season start", "new season",
            "weekly reset", "reset", "maintenance", "downtime",
            "hotfix", "tuning", "nerf", "buff", "balance changes",
            "class changes", "spec changes", "item level",
            "trading post", "catalyst", "creation catalyst",
            "delve", "world soul", "bountiful delve",
            "profession", "crafting", "knowledge point",
            "pvp season", "rated pvp", "arena", "conquest", "honor",
        ]
        timing_keywords = [
            "this week", "next week", "coming week", "upcoming",
            "starting", "ending", "begins", "concludes",
            "tuesday", "wednesday", "thursday", "friday",
            "tomorrow", "today", "soon", "incoming",
        ]
        high_priority = [
            "developer", "announcement", "upcoming changes",
            "ptr", "public test", "preview", "known issues",
        ]

        has_reset = any(k in combined for k in reset_keywords)
        has_timing = any(k in combined for k in timing_keywords)
        is_high_priority = any(k in combined for k in high_priority)
        return has_reset or (has_timing and is_high_priority)

    def summarize_reset_info(self, posts: List[Dict]) -> Dict:
        if not posts:
            return {}

        summary: Dict[str, List[Dict]] = {"this_week": [], "next_week": [], "general": []}
        for post in posts:
            title = post["title"]
            content = post.get("content_preview", "").lower()
            combined = f"{title.lower()} {content}"
            entry = {
                "title": title,
                "url": post.get("url"),
                "preview": content[:100] + "..." if len(content) > 100 else content,
            }
            if any(t in combined for t in ("this week", "starting", "begins", "today", "tomorrow")):
                summary["this_week"].append(entry)
            elif any(t in combined for t in ("next week", "upcoming", "coming", "soon")):
                summary["next_week"].append(entry)
            else:
                summary["general"].append(entry)
        return summary


def _text(item: ET.Element, tag: str) -> str:
    el = item.find(tag)
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _extract_region(link: str) -> str:
    match = re.search(r"/blue-tracker/topic/([a-z]{2,3})/", link, re.IGNORECASE)
    return match.group(1).lower() if match else ""


def _extract_post_id(guid: str, link: str) -> str:
    for candidate in (guid, link):
        match = re.search(r"/(\d+)(?:\?|$)", candidate or "")
        if match:
            return match.group(1)
    return guid or link


def _parse_pubdate(raw: str) -> Optional[datetime]:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _format_pubdate(dt: Optional[datetime], raw: str) -> str:
    if dt is not None:
        return dt.strftime("%B %d, %Y at %I:%M %p UTC")
    return raw or "Recently"


_TAG_RE = re.compile(r"<[^>]+>")
_IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _clean_description(html: str) -> str:
    if not html:
        return ""
    text = _TAG_RE.sub(" ", html)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*Continue reading\s*»\s*$", "", text, flags=re.IGNORECASE)
    return text[:200] + "..." if len(text) > 200 else text


def _first_img_src(html: str) -> Optional[str]:
    match = _IMG_SRC_RE.search(html or "")
    return match.group(1) if match else None
