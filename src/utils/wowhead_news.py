"""
Wowhead News RSS utility for relevant WoW articles.

Uses Wowhead's public RSS feed (https://www.wowhead.com/news/rss/all), which is
not behind Cloudflare bot protection, instead of scraping the HTML index page.
"""

import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

MEDIA_NS = "{http://search.yahoo.com/mrss/}"


class WowheadNewsScraper:
    def __init__(self) -> None:
        self.url = "https://www.wowhead.com/news/rss/all"
        self.cache_file = "wowhead_news_cache.json"
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
        return {"last_check": None, "seen_articles": []}

    def save_cache(self, cache_data: Dict) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.warning("Error saving cache: %s", e)

    def fetch_news_page(self) -> Optional[List[ET.Element]]:
        """Fetch the Wowhead news RSS feed and return its <item> elements."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            return root.findall(".//item")
        except (requests.RequestException, ET.ParseError) as e:
            logger.error("Error fetching Wowhead news feed: %s", e)
            return None

    def parse_articles(self, items: Optional[List[ET.Element]]) -> List[Dict]:
        """Normalize RSS <item> elements into article dicts and filter for relevance."""
        if not items:
            return []

        articles: List[Dict] = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for item in items[:25]:
            try:
                title = _text(item, "title")
                link = _text(item, "link")
                if not title or not link:
                    continue

                description = _text(item, "description")
                pub_date_raw = _text(item, "pubDate")
                category = _text(item, "category")
                guid = _text(item, "guid") or link

                media = item.find(f"{MEDIA_NS}content")
                image_url = media.get("url") if media is not None else None
                if not image_url and description:
                    image_url = _first_img_src(description)

                article = {
                    "title": title,
                    "url": link,
                    "author": category or "Wowhead Staff",
                    "time_posted": _format_pubdate(pub_date_raw),
                    "article_id": _extract_article_id(guid, link),
                    "scraped_at": now_iso,
                    "content_preview": _clean_description(description),
                    "image_url": image_url,
                }

                if self.is_relevant_article(article):
                    articles.append(article)
            except Exception as e:  # noqa: BLE001 - keep loop alive on bad item
                logger.warning("Error parsing news item: %s", e)
                continue

        return articles[:10]

    def is_relevant_article(self, article_data: Dict) -> bool:
        if not article_data or not article_data.get("title"):
            return False

        title = article_data["title"].lower()

        exclude_games = [
            "diablo", "overwatch", "hearthstone", "heroes of the storm",
            "starcraft", "call of duty", "candy crush",
        ]
        if any(game in title for game in exclude_games):
            return False

        wow_keywords = [
            "wow", "world of warcraft", "warcraft", "azeroth",
            "war within", "midnight", "worldsoul saga", "patch", "hotfix",
            "ptr", "public test", "alpha", "beta",
            "mythic+", "mythic plus", "m+", "affix", "affixes", "dungeon",
            "great vault", "vault", "weekly", "reset",
            "raid", "manaforge", "dimensius", "tier set", "tier token",
            "heroic", "mythic raid", "raid finder", "world first",
            "class", "spec", "specialization", "talent", "hero talent",
            "tuning", "nerf", "buff", "balance", "changes",
            "season", "delve", "world quest", "timewalking",
            "world boss", "bonus event", "pvp season",
            "profession", "crafting", "knowledge point", "catalyst",
            "sylvanas", "thrall", "jaina", "anduin", "xalatath",
            "silvermoon", "quel'thalas", "void", "light",
            "ion hazzikostas", "developer", "interview", "announcement",
            "blizzard", "gamescom", "blizzcon",
            "player housing", "housing", "demon hunter",
            "haranir", "earthen", "race", "racial",
        ]
        if any(keyword in title for keyword in wow_keywords):
            return True

        return any(keyword in title for keyword in ("mmo", "rpg", "expansion", "update", "announcement"))

    def is_reset_relevant(self, article_data: Dict) -> bool:
        if not article_data or not article_data.get("title"):
            return False

        title = article_data["title"].lower()
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
        return any(keyword in title for keyword in reset_keywords)

    def get_new_articles(self) -> List[Dict]:
        cache = self.load_cache()
        seen_articles = set(cache.get("seen_articles", []))
        is_first_run = len(seen_articles) == 0 and cache.get("last_check") is None

        items = self.fetch_news_page()
        if items is None:
            return []

        all_articles = self.parse_articles(items)
        new_articles: List[Dict] = []
        for article in all_articles:
            article_id = article.get("article_id", "")
            if article_id and article_id not in seen_articles:
                new_articles.append(article)
                seen_articles.add(article_id)

        if is_first_run and new_articles:
            logger.info("First run detected - returning %d most recent articles", min(3, len(new_articles)))
            new_articles = new_articles[:3]

        cache["seen_articles"] = list(seen_articles)
        cache["last_check"] = datetime.now(timezone.utc).isoformat()
        self.save_cache(cache)

        return new_articles

    def get_reset_relevant_articles(self, days_back: int = 7) -> List[Dict]:
        items = self.fetch_news_page()
        if items is None:
            return []

        all_articles = self.parse_articles(items)
        return [a for a in all_articles if self.is_reset_relevant(a)][:10]

    def summarize_reset_info(self, articles: List[Dict]) -> Dict:
        if not articles:
            return {}

        summary: Dict[str, List[Dict]] = {
            "mythic_plus": [],
            "raids": [],
            "events": [],
            "patches": [],
            "general": [],
        }

        for article in articles:
            title = article["title"].lower()
            entry = {
                "title": article["title"],
                "url": article["url"],
                "time": article.get("time_posted", "Recently"),
            }

            if any(term in title for term in ("mythic+", "mythic plus", "m+", "affix", "dungeon")):
                summary["mythic_plus"].append(entry)
            elif any(term in title for term in ("raid", "tier set", "manaforge", "dimensius")):
                summary["raids"].append(entry)
            elif any(term in title for term in ("hotfix", "patch", "tuning", "nerf", "buff")):
                summary["patches"].append(entry)
            elif any(term in title for term in ("event", "timewalking", "world boss", "bonus")):
                summary["events"].append(entry)
            else:
                summary["general"].append(entry)

        return summary


def _text(item: ET.Element, tag: str) -> str:
    el = item.find(tag)
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _format_pubdate(raw: str) -> str:
    if not raw:
        return "Recently"
    try:
        dt = parsedate_to_datetime(raw)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except (TypeError, ValueError):
        return raw


def _extract_article_id(guid: str, link: str) -> str:
    for candidate in (guid, link):
        if not candidate:
            continue
        match = re.search(r"news=?/?(\d+)", candidate)
        if match:
            return match.group(1)
    return guid or link


_TAG_RE = re.compile(r"<[^>]+>")
_IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _clean_description(html: str) -> str:
    if not html:
        return ""
    text = _TAG_RE.sub(" ", html)
    text = re.sub(r"\s+", " ", text).strip()
    # Strip the trailing "Continue reading »" sentinel the feed adds.
    text = re.sub(r"\s*Continue reading\s*»\s*$", "", text, flags=re.IGNORECASE)
    return text[:200] + "..." if len(text) > 200 else text


def _first_img_src(html: str) -> Optional[str]:
    match = _IMG_SRC_RE.search(html or "")
    return match.group(1) if match else None
