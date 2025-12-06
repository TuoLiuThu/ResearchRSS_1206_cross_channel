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
    # 新增频道
    {
        "name": "Google DeepMind",
        "channel_id": "UCP7jMXSY2xbc3KCAE0MHQ-A",
        "description": "DeepMind官方频道",
    },
    {
        "name": "Stanford HAI",
        "channel_id": "UCg1W32qTjayiCDzQ5VpQ0oQ",
        "description": "Stanford人工智能研究所",
    },
    {
        "name": "Google",
        "channel_id": "UCK1i2UviaXLUNrZlAFpw_jA",
        "description": "Google官方 (I/O, 发布会)",
    },
    {
        "name": "TED",
        "channel_id": "UCAuUUnT6oDeKwE6v1US3LqQ",
        "description": "TED演讲",
    },
    {
        "name": "a]6z",
        "channel_id": "UCBcRF18a7Qf58cCRy5xuWwQ",
        "description": "a16z 科技投资播客",
    },
    {
        "name": "Y Combinator",
        "channel_id": "UCcefcZRL2oaA_uBNeo5UOWg",
        "description": "YC创业访谈",
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
    # 新增RSS源
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "type": "news",
    },
    {
        "name": "The Information",
        "url": "https://www.theinformation.com/feed",
        "type": "news",
    },
    {
        "name": "Reuters Tech",
        "url": "https://www.reuters.com/technology/rss",
        "type": "news",
    },
    {
        "name": "Bloomberg Tech",
        "url": "https://feeds.bloomberg.com/technology/news.rss",
        "type": "news",
    },
]

# Configuration
# 扩大到168小时(7天)以增加发现概率，因为顶级访谈较少
LOOKBACK_HOURS = 75
MAX_RESULTS_PER_SOURCE = 15

