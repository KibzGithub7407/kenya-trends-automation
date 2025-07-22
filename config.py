# requirements.txt
pytrends==4.9.2
requests==2.31.0
python-dotenv==1.0.0
schedule==1.2.0
beautifulsoup4==4.12.2
lxml==4.9.3
pandas==2.0.3
numpy==1.24.3

# Optional: For social media posting
tweepy==4.14.0
facebook-sdk==3.1.0

# Optional: For advanced features
textblob==0.17.1
vaderSentiment==3.3.2
Pillow==10.0.0

# Optional: For notifications
yagmail==0.15.293

---

# config.py
"""
Configuration settings for Kenya Trends Automation
"""
import os
from typing import Dict, List

class Config:
    """Main configuration class"""
    
    # Google Trends Settings
    GOOGLE_TRENDS_GEO = 'KE'  # Kenya
    GOOGLE_TRENDS_LANG = 'en-KE'
    GOOGLE_TRENDS_TIMEZONE = 180  # UTC+3 (EAT)
    
    # Automation Settings
    MAX_KEYWORDS_PROCESS = 10
    MAX_POSTS_GENERATE = 5
    UPDATE_FREQUENCY_HOURS = 6
    
    # Rate Limiting
    REQUEST_DELAY = 2  # seconds between requests
    API_RETRY_ATTEMPTS = 3
    
    # Content Settings
    MIN_POST_LENGTH = 50
    MAX_POST_LENGTH = 280  # Twitter limit
    INCLUDE_HASHTAGS = True
    MAX_HASHTAGS = 5
    
    # File Paths
    DATA_DIR = 'data'
    LOGS_DIR = 'logs'
    TEMPLATES_DIR = 'templates'
    
    # Kenyan Hashtags
    KENYA_HASHTAGS = [
        '#Kenya', '#Nairobi', '#KenyaTrends', '#KOT', 
        '#TukoTogether', '#KenyaDaily', '#EastAfrica', 
        '#Kenyan', '#NairobiLife', '#KenyaNews',
        '#Mombasa', '#Kisumu', '#Eldoret', '#KenyaFirst'
    ]
    
    # Post Templates by Category
    POST_TEMPLATES = {
        'trending': [
            "🔥 What's hot in Kenya: '{keyword}' is trending! {context} #TrendingKenya",
            "📈 Kenyans can't stop talking about '{keyword}' - {context} #KOT #Kenya",
            "⚡ Breaking trend: '{keyword}' is taking over Kenya! {context} #Viral",
            "🇰🇪 Trending now: '{keyword}' - here's what Kenyans are saying {context}"
        ],
        'educational': [
            "📚 Trend explained: Why '{keyword}' is popular in Kenya {context} #Education",
            "💡 Understanding '{keyword}': {context} #LearnSomethingNew #Kenya",
            "🎓 Kenyan trend spotlight: '{keyword}' - {context} #KnowledgeIsWealth",
            "📖 Deep dive: '{keyword}' and its impact in Kenya {context}"
        ],
        'engagement': [
            "🤔 What's your take on '{keyword}' trending in Kenya? {context} #KenyaDebate",
            "📊 Quick poll: How do you feel about '{keyword}'? {context} #KenyaOpinion",
            "💬 Let's discuss '{keyword}' - what are your thoughts, KOT? {context}",
            "🗣️ Kenya speaks: Share your opinion on '{keyword}' {context} #Discussion"
        ],
        'news': [
            "📰 News update: '{keyword}' making headlines in Kenya {context} #KenyaNews",
            "🚨 Alert: '{keyword}' - here's what Kenyans need to know {context}",
            "📢 Update on '{keyword}': {context} #NewsUpdate #Kenya",
            "⚠️ Important: '{keyword}' trending - stay informed {context}"
        ]
    }
    
    # Kenyan Context Keywords for Better Localization
    KENYAN_CONTEXTS = {
        'politics': [
            'Bunge', 'Parliament', 'Senate', 'National Assembly', 
            'County Government', 'Governor', 'MP', 'MCA', 'President',
            'Deputy President', 'Cabinet Secretary', 'State House'
        ],
        'sports': [
            'Harambee Stars', 'FKF Premier League', 'Athletics Kenya',
            'Safari Rally', 'Kenyan Premier League', 'Tusker FC',
            'Gor Mahia', 'AFC Leopards', 'Olympics', 'Marathon'
        ],
        'entertainment': [
            'Kenyan music', 'Gengetone', 'Benga', 'Kapuka',
            'Churchill Show', 'KTN', 'Citizen TV', 'NTV',
            'Sauti Sol', 'Nyashinski', 'Bahati', 'Diana Marua',
            'Kenyan film', 'Riverwood', 'comedy', 'concert'
        ],
        'business': [
            'NSE', 'Nairobi Securities Exchange', 'SMEs', 'M-Pesa',
            'Safaricom', 'Equity Bank', 'KCB', 'Co-op Bank',
            'startup', 'fintech', 'agriculture', 'manufacturing',
            'tourism', 'tea export', 'coffee', 'horticulture'
        ],
        'education': [
            'KCSE', 'KCPE', 'CBC', 'university', 'HELB',
            'University of Nairobi', 'Kenyatta University', 'Strathmore',
            'TVET', 'technical training', 'scholarship', 'education CS'
        ],
        'technology': [
            'digital transformation', 'internet', 'mobile money',
            'fiber optic', '5G Kenya', 'tech hub', 'innovation',
            'Silicon Savannah', 'iHub', 'startup ecosystem'
        ],
        'health': [
            'Ministry of Health', 'COVID-19 Kenya', 'vaccination',
            'Kenyatta Hospital', 'Moi Teaching Hospital', 'healthcare',
            'medical insurance', 'NHIF', 'public health'
        ],
        'culture': [
            'Swahili', 'Kikuyu', 'Luo', 'Kalenjin', 'Luhya',
            'cultural festival', 'heritage', 'traditional dance',
            'Kenyan culture', 'tribal', 'unity', 'diversity'
        ]
    }
    
    # Time zones and optimal posting times (EAT - East Africa Time)
    OPTIMAL_POSTING_TIMES = [
        {'hour': 7, 'minute': 0},   # 7:00 AM
        {'hour': 12, 'minute': 30}, # 12:30 PM
        {'hour': 18, 'minute': 0},  # 6:00 PM
        {'hour': 20, 'minute': 30}  # 8:30 PM
    ]
    
    # Content filtering - avoid sensitive topics
    FILTERED_KEYWORDS = [
        'terrorism', 'violence', 'hate speech', 'discrimination',
        'explicit content', 'illegal activities', 'fake news'
    ]
    
    @classmethod
    def get_template_by_category(cls, category: str) -> List[str]:
        """Get post templates by category"""
        return cls.POST_TEMPLATES.get(category, cls.POST_TEMPLATES['trending'])
    
    @classmethod
    def get_kenyan_context(cls, keyword: str) -> str:
        """Get Kenyan context for a keyword"""
        keyword_lower = keyword.lower()
        
        for category, contexts in cls.KENYAN_CONTEXTS.items():
            for context in contexts:
                if context.lower() in keyword_lower:
                    return f"Related to {category} in Kenya"
        
        return "Trending topic in Kenya"

---

# post_templates.json
{
  "trending_kenya": {
    "general": [
      "🔥 Kenya is buzzing! '{keyword}' is the hottest trend right now. {context} #KenyaTrends #Nairobi",
      "📈 What's got Kenyans talking? '{keyword}' is trending nationwide! {context} #KOT #TrendingNow",
      "⚡ Alert: '{keyword}' is taking Kenya by storm! {context} #ViralKenya #Trending",
      "🇰🇪 From Mombasa to Kisumu, everyone's discussing '{keyword}' {context} #OneKenya"
    ],
    "morning": [
      "☀️ Good morning Kenya! Starting the day with '{keyword}' trending {context} #MorningTrends #Kenya",
      "🌅 Rise and shine! '{keyword}' is what Kenyans are waking up to {context} #GoodMorningKenya"
    ],
    "evening": [
      "🌆 As the sun sets, '{keyword}' lights up Kenyan social media {context} #EveningTrends",
      "🌙 End of day update: '{keyword}' still trending strong in Kenya {context} #KenyaNights"
    ]
  },
  "educational_content": {
    "explainer": [
      "📚 Let's break it down: Why '{keyword}' matters to Kenya {context} #EducateKenya #LearnTogether",
      "💡 Quick lesson: Understanding '{keyword}' and its Kenyan context {context} #KnowledgeSharing",
      "🎓 Educational moment: '{keyword}' explained for every Kenyan {context} #ElimuKenya"
    ],
    "facts": [
      "📊 Did you know? Facts about '{keyword}' every Kenyan should know {context} #FactCheck #Kenya",
      "🔍 Research shows: '{keyword}' insights for Kenyan audiences {context} #DataDriven"
    ]
  },
  "engagement_posts": {
    "questions": [
      "🤔 Kenya decides: What's your stance on '{keyword}'? Share below! {context} #KenyaDecides",
      "❓ Question for KOT: How does '{keyword}' affect your daily life? {context} #KOTDiscussion",
      "💭 Thinking aloud: Is '{keyword}' good or bad for Kenya? Your thoughts? {context} #KenyaThinks"
    ],
    "polls": [
      "📊 Poll time! Rate '{keyword}' impact on Kenya: 👍 Positive 👎 Negative {context} #KenyaPoll",
      "🗳️ Your vote counts: Should Kenya embrace '{keyword}'? Yes/No in comments {context} #VoteKenya"
    ]
  },
  "news_updates": {
    "breaking": [
      "🚨 Breaking: '{keyword}' developing story in Kenya {context} #BreakingNews #Kenya",
      "📰 News Alert: '{keyword}' - here's what we know so far {context} #KenyaNews #Update"
    ],
    "analysis": [
      "🔎 In-depth: How '{keyword}' is shaping Kenya's future {context} #Analysis #KenyaFuture",
      "📈 Trend Analysis: '{keyword}' impact on Kenyan society {context} #TrendAnalysis"
    ]
  },
  "cultural_local": {
    "swahili_touch": [
      "🇰🇪 Haya jamani! '{keyword}' ni trending sana Kenya! {context} #SwahiliTrends #Kenya",
      "✨ Pole pole, lakini '{keyword}' inashika Kenya kwa nguvu! {context} #KiswahiliVibes"
    ],
    "regional": [
      "🏔️ From Mt. Kenya to the Coast: '{keyword}' unites all regions {context} #UnityInDiversity",
      "🌊 Coastal to Highland: '{keyword}' resonates across Kenya {context} #Kenya254"
    ]
  }
}

---

# .github/workflows/kenya-trends-bot.yml
name: Kenya Trends Social Media Bot

on:
  schedule:
    # Run 4 times a day at optimal East Africa Time
    - cron: '0 4 * * *'   # 7 AM EAT (4 AM UTC)
    - cron: '30 9 * * *'  # 12:30 PM EAT (9:30 AM UTC)  
    - cron: '0 15 * * *'  # 6 PM EAT (3 PM UTC)
    - cron: '30 17 * * *' # 8:30 PM EAT (5:30 PM UTC)
  
  workflow_dispatch: # Manual trigger
    inputs:
      post_count:
        description: 'Number of posts to generate'
        required: false
        default: '5'
      test_mode:
        description: 'Run in test mode (no posting)'
        required: false
        default: 'true'

jobs:
  generate-kenya-trends-posts:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Create necessary directories
      run: |
        mkdir -p data logs templates
        
    - name: Run Kenya Trends Automation
      env:
        TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
        TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
        TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
        TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
        FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
        LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
        TEST_MODE: ${{ github.event.inputs.test_mode || 'true' }}
        POST_COUNT: ${{ github.event.inputs.post_count || '5' }}
      run: |
        python main.py
        
    - name: Upload generated data
      uses: actions/upload-artifact@v3
      with:
        name: kenya-trends-data-${{ github.run_number }}
        path: |
          data/
          logs/
        retention-days: 30
        
    - name: Send notification on failure
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          const issue_title = `Kenya Trends Bot Failed - Run #${context.runNumber}`;
          const issue_body = `
          The Kenya Trends automation failed on ${new Date().toISOString()}.
          
          **Run Details:**
          - Workflow: ${context.workflow}
          - Run Number: ${context.runNumber}
          - Commit: ${context.sha.substring(0, 7)}
          
          Please check the logs for more details.
          `;
          
          // Create an issue (optional)
          await github.rest.issues.create({
            owner: context.repo.owner,
            repo: context.repo.repo,
            title: issue_title,
            body: issue_body,
            labels: ['bug', 'automation']
          });

---

# Procfile (for Heroku deployment)
worker: python main.py
web: python -m http.server $PORT

---

# railway.toml (for Railway deployment)
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python main.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[env]
PYTHON_VERSION = "3.9"

---

# docker-compose.yml (for Docker deployment)
version: '3.8'

services:
  kenya-trends-bot:
    build: .
    environment:
      - TWITTER_API_KEY=${TWITTER_API_KEY}
      - TWITTER_API_SECRET=${TWITTER_API_SECRET}
      - TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN}
      - TWITTER_ACCESS_TOKEN_SECRET=${TWITTER_ACCESS_TOKEN_SECRET}
      - FACEBOOK_ACCESS_TOKEN=${FACEBOOK_ACCESS_TOKEN}
      - LINKEDIN_ACCESS_TOKEN=${LINKEDIN_ACCESS_TOKEN}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    command: python main.py

---

# Dockerfile (for containerization)
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs templates

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]

---

# .gitignore
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Data and logs
data/*.json
logs/*.log
*.csv
*.xlsx

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
temp/
tmp/
*.tmp

# API keys and secrets (backup)
secrets.txt
api_keys.txt
credentials.json
            '
