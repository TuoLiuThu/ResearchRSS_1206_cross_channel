"""
Web Scraper Module
网页抓取模块 - 获取文章和视频的完整内容
"""

import os
import logging
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, 
    NoTranscriptFound,
    VideoUnavailable
)

logger = logging.getLogger(__name__)

# Request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_youtube_transcript(video_id: str) -> str:
    """
    Get transcript from YouTube video.
    获取YouTube视频字幕
    """
    if not video_id:
        return ""
    
    try:
        # Try to get transcript in order of preference
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Prefer manually created transcripts over auto-generated
        transcript = None
        
        try:
            # Try English first
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            try:
                # Try any manually created transcript
                transcript = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
            except NoTranscriptFound:
                try:
                    # Fall back to auto-generated
                    transcript = transcript_list.find_generated_transcript(['en'])
                except NoTranscriptFound:
                    # Try to get any available transcript and translate
                    try:
                        available = list(transcript_list)
                        if available:
                            transcript = available[0].translate('en')
                    except Exception:
                        pass
        
        if transcript:
            entries = transcript.fetch()
            full_text = " ".join([entry['text'] for entry in entries])
            logger.info(f"Got transcript for video {video_id}: {len(full_text)} chars")
            return full_text
            
    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video {video_id}")
    except VideoUnavailable:
        logger.warning(f"Video unavailable: {video_id}")
    except Exception as e:
        logger.error(f"Error getting transcript for {video_id}: {e}")
    
    return ""


def get_article_content(url: str) -> str:
    """
    Get article content from URL.
    从URL获取文章内容
    """
    if not url:
        return ""
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.decompose()
        
        # Try to find main content area
        content = None
        
        # Common article containers
        selectors = [
            'article',
            '[role="main"]',
            '.post-content',
            '.article-content',
            '.entry-content',
            '.content',
            'main',
        ]
        
        for selector in selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        if not content:
            content = soup.body
        
        if content:
            # Get text while preserving some structure
            text = content.get_text(separator='\n', strip=True)
            
            # Clean up multiple newlines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            
            # Truncate if too long
            if len(text) > 50000:
                text = text[:50000] + "..."
            
            logger.info(f"Got article content from {url}: {len(text)} chars")
            return text
            
    except requests.RequestException as e:
        logger.error(f"Error fetching article {url}: {e}")
    except Exception as e:
        logger.error(f"Error parsing article {url}: {e}")
    
    return ""


def scrape_content(item: dict) -> dict:
    """
    Scrape full content for a discovered item.
    为发现的内容项抓取完整内容
    """
    source_type = item.get('source_type', '')
    
    if source_type == 'youtube':
        video_id = item.get('video_id')
        if video_id:
            transcript = get_youtube_transcript(video_id)
            item['content'] = transcript
            item['content_type'] = 'transcript' if transcript else 'description_only'
            
            if not transcript:
                # Fall back to description
                item['content'] = item.get('description', '')
    else:
        # Article/blog content
        url = item.get('url', '')
        if url:
            article_content = get_article_content(url)
            item['content'] = article_content
            item['content_type'] = 'article' if article_content else 'summary_only'
            
            if not article_content:
                item['content'] = item.get('description', '')
    
    return item


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with a sample video
    test_video_id = "dQw4w9WgXcQ"  # Rick Astley - for testing
    transcript = get_youtube_transcript(test_video_id)
    print(f"Transcript length: {len(transcript)}")
    print(f"First 200 chars: {transcript[:200]}")
