#!/usr/bin/env python3
"""
AI Expert Interview Aggregator - Main Entry Point
AI 顶尖专家访谈聚合器 - 主入口

This script orchestrates the entire daily digest workflow:
1. Discover content from YouTube and RSS feeds
2. Scrape full content (transcripts, articles)
3. Summarize using Gemini (bilingual: EN + CN)
4. Send email report
"""

import os
import sys
import logging
import argparse
import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.discovery import discover_content
from src.scraper import scrape_content
from src.summarizer import summarize_content
from src.notifier import generate_html_report, send_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="AI Expert Interview Aggregator - Daily Digest"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Save report to file instead of sending email"
    )
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🧠 AI Expert Interview Aggregator Starting...")
    logger.info("=" * 60)
    
    # Phase 1: Discovery
    logger.info("\n📡 Phase 1: Content Discovery")
    logger.info("-" * 40)
    discovered_items = discover_content()
    
    if not discovered_items:
        logger.info("No matching content found in last 24 hours.")
        # Still send an email to confirm the system is working
        html_report = generate_html_report([])
        
        if args.dry_run:
            with open("dry_run_report.html", "w", encoding="utf-8") as f:
                f.write(html_report)
            logger.info("Empty report saved to dry_run_report.html")
        else:
            beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
            date_str = datetime.datetime.now(beijing_tz).strftime("%Y-%m-%d")
            subject = f"🧠 AI Expert Daily Digest | {date_str} | No Updates"
            send_email(subject, html_report)
        
        logger.info("Job complete (no content found).")
        return
    
    logger.info(f"✅ Discovered {len(discovered_items)} items")
    
    # Phase 2: Scraping
    logger.info("\n📄 Phase 2: Content Scraping")
    logger.info("-" * 40)
    scraped_items = []
    
    for item in discovered_items:
        logger.info(f"Scraping: {item['title'][:50]}...")
        scraped_item = scrape_content(item)
        if scraped_item and scraped_item.get('content'):
            scraped_items.append(scraped_item)
        else:
            logger.warning(f"No content extracted for: {item['title']}")
    
    logger.info(f"✅ Scraped {len(scraped_items)} items with content")
    
    if not scraped_items:
        logger.info("No content could be scraped.")
        return
    
    # Phase 3: Summarization
    logger.info("\n🤖 Phase 3: AI Summarization (Gemini)")
    logger.info("-" * 40)
    summarized_items = []
    
    for item in scraped_items:
        logger.info(f"Summarizing: {item['title'][:50]}...")
        summarized_item = summarize_content(item)
        if summarized_item:
            summarized_items.append(summarized_item)
        else:
            logger.warning(f"Summarization failed for: {item['title']}")
    
    logger.info(f"✅ Summarized {len(summarized_items)} items")
    
    # Phase 4: Notification
    logger.info("\n📧 Phase 4: Email Notification")
    logger.info("-" * 40)
    
    if summarized_items:
        html_report = generate_html_report(summarized_items)
        
        beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
        date_str = datetime.datetime.now(beijing_tz).strftime("%Y-%m-%d")
        subject = f"🧠 AI Expert Daily Digest | {date_str} | {len(summarized_items)} Updates"
        
        if args.dry_run:
            with open("dry_run_report.html", "w", encoding="utf-8") as f:
                f.write(html_report)
            logger.info("✅ Report saved to dry_run_report.html (dry-run mode)")
        else:
            success = send_email(subject, html_report)
            if success:
                logger.info("✅ Email sent successfully!")
            else:
                logger.warning("Email sending failed, report saved to latest_report.html")
    else:
        logger.info("No items to report after processing.")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 Job Complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
