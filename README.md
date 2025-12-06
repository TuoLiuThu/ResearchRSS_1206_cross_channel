# AI Expert Interview Aggregator
# AI 顶尖专家访谈聚合器

[![Daily Digest](https://github.com/TuoLiuThu/ai-expert-aggregator/actions/workflows/daily_digest.yml/badge.svg)](https://github.com/TuoLiuThu/ai-expert-aggregator/actions/workflows/daily_digest.yml)

自动聚合17位AI领域顶尖科学家的访谈、文章和论文，每天北京时间8:00发送双语日报邮件。

Automatically aggregate interviews, articles, and papers from 17 top AI scientists. Sends bilingual daily digest at 8:00 AM Beijing Time.

---

## 🧠 Tracked Scientists | 追踪的科学家

| Organization | Name | Role |
|--------------|------|------|
| **OpenAI** | Alec Radford | Distinguished Researcher |
| | Jakub Pachocki | Chief Scientist |
| | John Schulman | Co-founder (now at Anthropic) |
| | Mark Chen | VP of Research |
| **DeepMind** | Demis Hassabis | CEO |
| | Jeff Dean | Google Chief Scientist |
| | Oriol Vinyals | VP of Research |
| **Anthropic** | Dario Amodei | CEO |
| | Jared Kaplan | Co-founder |
| | Chris Olah | Co-founder |
| **xAI** | Igor Babuschkin | Core Tech Lead |
| | Christian Szegedy | Founding Member |
| | Zihang Dai | Founding Member |
| | Guodong Zhang | Founding Member |
| **Independent** | Ilya Sutskever | SSI Founder |
| | Bill Dally | NVIDIA Chief Scientist |
| | Fei-Fei Li | Stanford Professor |

---

## 🚀 Quick Start | 快速开始

### Step 1: Fork this Repository

Click the **Fork** button at the top right of this page.

### Step 2: Get API Keys | 获取 API 密钥

#### 2.1 Gemini API Key (Free)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **Create API Key**
3. Copy and save the key

#### 2.2 YouTube Data API Key (Free)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **YouTube Data API v3**:
   - Go to APIs & Services → Library
   - Search "YouTube Data API v3" → Enable
4. Create credentials:
   - Go to APIs & Services → Credentials
   - Click **Create Credentials** → **API Key**
5. Copy and save the key

#### 2.3 Gmail App Password
1. Enable 2-Step Verification on your Google Account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** and **Windows Computer**
4. Click **Generate** and copy the 16-character password

### Step 3: Configure GitHub Secrets

Go to your forked repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

| Secret Name | Description |
|-------------|-------------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `YOUTUBE_API_KEY` | Your YouTube Data API key |
| `EMAIL_SENDER` | Your Gmail address |
| `EMAIL_PASSWORD` | Gmail app password (16 chars) |
| `EMAIL_RECIPIENT` | Email to receive daily digest |

### Step 4: Enable GitHub Actions

Go to **Actions** tab → Click **I understand my workflows, go ahead and enable them**

### Step 5: Test Run | 测试运行

Go to **Actions** → **Daily AI Expert Digest** → **Run workflow** → **Run workflow**

Check your email in a few minutes!

---

## ⏰ Schedule | 定时任务

The workflow runs automatically at:
- **8:00 AM Beijing Time (UTC+8)** = **0:00 UTC**

You can also manually trigger it anytime from the Actions tab.

---

## 📧 Email Report Format | 邮件报告格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 AI Expert Daily Digest | 2025-12-06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Demis Hassabis (DeepMind CEO)
🎬 Video Interview

【English Summary】
Demis discussed AlphaFold's impact on drug discovery...

【中文总结】
Demis 讨论了 AlphaFold 对药物研发的影响...

🔗 Link: https://youtube.com/watch?v=xxx
🎥 Video: https://youtube.com/watch?v=xxx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 Local Development | 本地开发

```bash
# Clone
git clone https://github.com/TuoLiuThu/ai-expert-aggregator.git
cd ai-expert-aggregator

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_key"
export YOUTUBE_API_KEY="your_key"
export EMAIL_SENDER="your_email"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECIPIENT="recipient_email"

# Run (dry-run mode, saves HTML report locally)
python main.py --dry-run

# Run (sends email)
python main.py
```

---

## 📁 Project Structure | 项目结构

```
ai-expert-aggregator/
├── .github/workflows/
│   └── daily_digest.yml    # GitHub Actions workflow
├── config/
│   ├── scientists.py       # Scientist list & tracking config
│   └── sources.py          # Data source configuration
├── src/
│   ├── discovery.py        # Content discovery module
│   ├── scraper.py          # Web scraping module
│   ├── summarizer.py       # Gemini bilingual summarization
│   └── notifier.py         # Email notification
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚠️ Limitations | 限制说明

1. **Low-profile scientists**: Some scientists (e.g., Alec Radford, Ilya Sutskever) rarely appear in public media
2. **API quotas**: YouTube API has daily limits (10,000 units/day)
3. **Content availability**: Not all interviews have transcripts available

---

## 📄 License

MIT License
