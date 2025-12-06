"""
Content Discovery Module
内容发现模块 - 从YouTube、RSS等渠道发现与科学家相关的内容
"""

import os
import logging
import datetime
from datetime import timezone, timedelta
from dateutil import parser as date_parser
import feedparser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    SCIENTISTS, get_all_aliases,
    YOUTUBE_CHANNELS, RSS_FEEDS, 
    LOOKBACK_HOURS, MAX_RESULTS_PER_SOURCE
)

logger = logging.getLogger(__name__)


def is_recent(published_date: datetime.datetime) -> bool:
    """
    Check if content was published within the lookback period.
    检查内容是否在回溯期内发布
    """
    if published_date is None:
        return False
    
    now = datetime.datetime.now(timezone.utc)
    
    # Ensure timezone aware
    if published_date.tzinfo is None:
        published_date = published_date.replace(tzinfo=timezone.utc)
    
    cutoff = now - timedelta(hours=LOOKBACK_HOURS)
    return published_date >= cutoff


def matches_scientist(text: str) -> list:
    """
    Check if text mentions any tracked scientist.
    检查文本是否提及任何追踪的科学家
    Returns list of matched scientist names.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    matched = []
    
    for name, info in SCIENTISTS.items():
        aliases = info.get("aliases", [name])
        for alias in aliases:
            if alias.lower() in text_lower:
                if name not in matched:
                    matched.append(name)
                break
    
    return matched


def get_youtube_videos() -> list:
    """
    Fetch recent videos from tracked YouTube channels that mention scientists.
    从追踪的YouTube频道获取提及科学家的近期视频
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.warning("YOUTUBE_API_KEY not set, skipping YouTube discovery")
        return []
    
    results = []
    
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Calculate cutoff time
        now = datetime.datetime.now(timezone.utc)
        published_after = (now - timedelta(hours=LOOKBACK_HOURS)).isoformat().replace('+00:00', 'Z')
        
        for channel in YOUTUBE_CHANNELS:
            logger.info(f"Checking YouTube channel: {channel['name']}")
            
            try:
                request = youtube.search().list(
                    part="snippet",
                    channelId=channel["channel_id"],
                    order="date",
                    publishedAfter=published_after,
                    type="video",
                    maxResults=MAX_RESULTS_PER_SOURCE
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    video_id = item['id']['videoId']
                    snippet = item['snippet']
                    title = snippet['title']
                    description = snippet.get('description', '')
                    
                    # Check if video mentions any scientist
                    search_text = f"{title} {description}"
                    matched_scientists = matches_scientist(search_text)
                    
                    if matched_scientists:
                        published_at = date_parser.parse(snippet['publishedAt'])
                        
                        logger.info(f"Found matching video: {title} -> {matched_scientists}")
                        
                        results.append({
                            "title": title,
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                            "video_id": video_id,
                            "video_url": f"https://www.youtube.com/watch?v={video_id}",
                            "description": description,
                            "published_at": published_at.isoformat(),
                            "source_name": channel['name'],
                            "source_type": "youtube",
                            "matched_scientists": matched_scientists,
                        })
                        
            except HttpError as e:
                logger.error(f"YouTube API error for {channel['name']}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"YouTube discovery error: {e}")
    
    return results


def get_rss_articles() -> list:
    """
    Fetch recent articles from RSS feeds that mention scientists.
    从RSS订阅获取提及科学家的近期文章
    """
    results = []
    
    for feed_config in RSS_FEEDS:
        logger.info(f"Checking RSS feed: {feed_config['name']}")
        
        try:
            feed = feedparser.parse(feed_config['url'])
            
            if feed.bozo:
                logger.warning(f"RSS parse issue for {feed_config['name']}: {feed.bozo_exception}")
            
            for entry in feed.entries[:MAX_RESULTS_PER_SOURCE]:
                # Parse publication date
                published_dt = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_dt = datetime.datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_dt = datetime.datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                
                # Skip if not recent
                if not is_recent(published_dt):
                    continue
                
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                
                # Check if mentions any scientist
                search_text = f"{title} {summary}"
                matched_scientists = matches_scientist(search_text)
                
                if matched_scientists:
                    logger.info(f"Found matching article: {title} -> {matched_scientists}")
                    
                    results.append({
                        "title": title,
                        "url": entry.get('link', ''),
                        "description": summary[:500],  # Truncate
                        "published_at": published_dt.isoformat() if published_dt else None,
                        "source_name": feed_config['name'],
                        "source_type": feed_config['type'],
                        "matched_scientists": matched_scientists,
                    })
                    
        except Exception as e:
            logger.error(f"RSS error for {feed_config['name']}: {e}")
            continue
    
    return results


def discover_content() -> list:
    """
    Main discovery function - aggregate content from all sources.
    主发现函数 - 从所有渠道聚合内容
    """
    all_content = []
    
    # YouTube videos
    logger.info("=== Discovering YouTube content ===")
    youtube_content = get_youtube_videos()
    all_content.extend(youtube_content)
    
    # RSS articles
    logger.info("=== Discovering RSS content ===")
    rss_content = get_rss_articles()
    all_content.extend(rss_content)
    
    # Remove duplicates by URL
    seen_urls = set()
    unique_content = []
    for item in all_content:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_content.append(item)
    
    logger.info(f"Discovery complete. Found {len(unique_content)} unique items.")
    return unique_content


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = discover_content()
    for item in results:
        print(f"- [{item['source_type']}] {item['title']}")
        print(f"  Scientists: {item['matched_scientists']}")
        print(f"  URL: {item['url']}")
        print()
