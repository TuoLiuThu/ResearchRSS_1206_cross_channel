"""
Notifier Module - Email notification with HTML report
通知模块 - HTML邮件报告
"""

import os
import smtplib
import datetime
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCIENTISTS

logger = logging.getLogger(__name__)


def generate_html_report(items: list) -> str:
    """
    Generate beautiful HTML email report.
    生成精美的HTML邮件报告
    """
    # Beijing time
    beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
    date_str = datetime.datetime.now(beijing_tz).strftime("%Y-%m-%d")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header .date {{
            opacity: 0.9;
            font-size: 16px;
        }}
        .header .summary {{
            margin-top: 15px;
            font-size: 14px;
            opacity: 0.85;
        }}
        .content {{
            padding: 30px;
        }}
        .item {{
            background: #fafafa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 4px solid #667eea;
        }}
        .item-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        .scientist-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }}
        .org-badge {{
            background: #e8e8e8;
            color: #555;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }}
        .source-badge {{
            background: #4CAF50;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: auto;
        }}
        .source-badge.video {{ background: #FF5722; }}
        .source-badge.article {{ background: #2196F3; }}
        .source-badge.podcast {{ background: #9C27B0; }}
        .item h2 {{
            margin: 0 0 15px 0;
            font-size: 18px;
            font-weight: 600;
        }}
        .item h2 a {{
            color: #1a1a1a;
            text-decoration: none;
        }}
        .item h2 a:hover {{
            color: #667eea;
        }}
        .section-title {{
            font-weight: 600;
            color: #667eea;
            margin: 15px 0 8px 0;
            font-size: 14px;
        }}
        .summary-text {{
            color: #333;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        .key-points {{
            background: #f0f4ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }}
        .key-points ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .key-points li {{
            margin-bottom: 5px;
            font-size: 13px;
        }}
        .links {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-size: 14px;
        }}
        .links a {{
            color: #667eea;
            text-decoration: none;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #888;
            font-size: 12px;
            background: #fafafa;
        }}
        .no-items {{
            text-align: center;
            padding: 50px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 AI Expert Daily Digest</h1>
            <div class="date">{date_str} | 北京时间 08:00</div>
            <div class="summary">追踪17位AI顶尖科学家的最新动态</div>
        </div>
        <div class="content">
"""

    if not items:
        html += """
            <div class="no-items">
                <h2>📭 No Updates Today</h2>
                <p>今日未发现追踪科学家的新访谈或文章</p>
                <p>No interviews or articles found for tracked scientists in the last 24 hours.</p>
            </div>
"""
    else:
        for item in items:
            scientist_name = item.get('scientist_name', item.get('matched_scientists', ['Unknown'])[0])
            scientist_info = SCIENTISTS.get(scientist_name, {})
            org = item.get('scientist_org', scientist_info.get('org', ''))
            
            source_type = item.get('source_type', 'article')
            source_class = 'video' if source_type in ['youtube', 'video'] else 'article'
            
            summary_en = item.get('summary_en', 'No summary available.')
            summary_cn = item.get('summary_cn', '暂无总结。')
            key_points = item.get('key_points', [])
            
            url = item.get('url', '#')
            video_url = item.get('video_url', '')
            
            html += f"""
            <div class="item">
                <div class="item-header">
                    <span class="scientist-badge">📌 {scientist_name}</span>
                    <span class="org-badge">{org}</span>
                    <span class="source-badge {source_class}">{source_type.upper()}</span>
                </div>
                <h2><a href="{url}" target="_blank">{item.get('title', 'Untitled')}</a></h2>
                
                <div class="section-title">【English Summary】</div>
                <div class="summary-text">{summary_en}</div>
                
                <div class="section-title">【中文总结】</div>
                <div class="summary-text">{summary_cn}</div>
"""
            
            if key_points:
                html += """
                <div class="key-points">
                    <div class="section-title" style="margin-top: 0;">🔑 Key Points</div>
                    <ul>
"""
                for point in key_points[:5]:
                    html += f"                        <li>{point}</li>\n"
                html += """                    </ul>
                </div>
"""
            
            html += f"""
                <div class="links">
                    🔗 <a href="{url}" target="_blank">原文链接 | Original Link</a>
"""
            if video_url and video_url != url:
                html += f"""
                    &nbsp;&nbsp;|&nbsp;&nbsp;🎥 <a href="{video_url}" target="_blank">视频源 | Video Source</a>
"""
            html += """
                </div>
            </div>
"""

    html += """
        </div>
        <div class="footer">
            <p>Generated by AI Expert Aggregator | GitHub Actions</p>
            <p>追踪科学家: OpenAI, DeepMind, Anthropic, xAI, 及独立专家</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def send_email(subject: str, html_body: str) -> bool:
    """
    Send email via SMTP (Gmail).
    通过SMTP发送邮件
    """
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    recipient = os.environ.get("EMAIL_RECIPIENT")
    
    if not all([sender, password, recipient]):
        logger.warning("Email config incomplete. Saving to file instead.")
        with open("latest_report.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        logger.info("Report saved to latest_report.html")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        logger.info(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        # Save to file as fallback
        with open("latest_report.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with sample data
    test_items = [
        {
            "title": "Demis Hassabis on AlphaFold and AGI",
            "scientist_name": "Demis Hassabis",
            "scientist_org": "DeepMind",
            "source_type": "interview",
            "url": "https://example.com/interview",
            "video_url": "https://youtube.com/watch?v=xxx",
            "summary_en": "Demis Hassabis discussed the future of AI and the impact of AlphaFold on drug discovery...",
            "summary_cn": "Demis Hassabis 讨论了AI的未来以及AlphaFold对药物研发的影响...",
            "key_points": [
                "AlphaFold has solved the protein folding problem",
                "AGI is potentially 5-10 years away",
                "AI safety is crucial for beneficial AGI",
            ],
        }
    ]
    
    html = generate_html_report(test_items)
    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Test report saved to test_report.html")
