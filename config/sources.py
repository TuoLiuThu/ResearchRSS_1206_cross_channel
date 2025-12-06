"""
Data sources configuration for AI Expert Aggregator
数据源配置
"""

# YouTube channels that frequently interview AI experts
YOUTUBE_CHANNELS = [
    {
        "name": "Lex Fridman Podcast",
        "channel_id": "UCSHZKyawb77ixDdsGog4iWA",
        "description": "深度AI专家访谈",
    },
    {
        "name": "Dwarkesh Podcast",
        "channel_id": "UCXl4i9dYBrFOabk0xGmbkRA",
        "description": "技术深度访谈",
    },
    {
        "name": "Machine Learning Street Talk",
        "channel_id": "UCMLtBahI5DMrt0NPvDSoIRQ",
        "description": "ML研究讨论",
    },
    {
        "name": "AI Explained",
        "channel_id": "UCNJ1Ymd5yFuUPtn21xtRbbw",
        "description": "AI新闻分析",
    },
    {
        "name": "Two Minute Papers",
        "channel_id": "UCbfYPyITQ-7l4upoX8nvctg",
        "description": "论文解读",
    },
    {
        "name": "No Priors Podcast",
        "channel_id": "UCMwQWNJGvrSkYgjUdlzKnaw",
        "description": "科技投资视角",
    },
    {
        "name": "The Logan Bartlett Show",
        "channel_id": "UCKyRB3AWHWLWB5JKd4pJxeA",
        "description": "科技创业访谈",
    },
    {
        "name": "Weights & Biases",
        "channel_id": "UCBcMWTDE19JXYKpxxnY7yGQ",
        "description": "ML工程访谈",
    },
]

# RSS feeds for tech news and podcasts
RSS_FEEDS = [
    {
        "name": "MIT Technology Review - AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "type": "news",
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "type": "news",
    },
    {
        "name": "The Verge - AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "type": "news",
    },
    {
        "name": "Wired - AI",
        "url": "https://www.wired.com/feed/tag/ai/latest/rss",
        "type": "news",
    },
    {
        "name": "Ars Technica - AI",
        "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "type": "news",
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "type": "blog",
    },
    {
        "name": "DeepMind Blog",
        "url": "https://deepmind.google/blog/rss.xml",
        "type": "blog",
    },
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news/rss",
        "type": "blog",
    },
]

# Configuration
LOOKBACK_HOURS = 80  # Slightly more than 24h to ensure we catch everything
MAX_RESULTS_PER_SOURCE = 10

