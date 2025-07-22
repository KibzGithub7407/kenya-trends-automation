#!/usr/bin/env python3
"""
Google Trends Kenya Social Media Post Generator
Automated system to fetch trending data and generate social media content
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import schedule
import time

# Required installations:
# pip install pytrends requests python-dotenv schedule

try:
    from pytrends.request import TrendReq
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Please install required packages:")
    print("pip install pytrends requests python-dotenv schedule")
    exit(1)

# Load environment variables
load_dotenv()

class GoogleTrendsKenya:
    def __init__(self):
        """Initialize the Google Trends Kenya fetcher"""
        self.pytrends = TrendReq(hl='en-KE', tz=180)  # Kenya timezone
        self.kenya_geo = 'KE'  # Kenya country code
        
    def get_trending_searches(self, days_back: int = 1) -> List[str]:
        """Get trending searches for Kenya"""
        try:
            # Get daily trending searches
            trending_searches = self.pytrends.trending_searches(pn='kenya')
            if not trending_searches.empty:
                # Return top 10 trending searches
                return trending_searches[0].head(10).tolist()
            return []
        except Exception as e:
            print(f"Error fetching trending searches: {e}")
            return []
    
    def get_interest_over_time(self, keywords: List[str]) -> Dict:
        """Get interest over time for specific keywords in Kenya"""
        try:
            if not keywords:
                return {}
                
            # Build payload for Kenya
            self.pytrends.build_payload(
                kw_list=keywords[:5],  # Max 5 keywords
                cat=0,
                timeframe='now 7-d',  # Last 7 days
                geo=self.kenya_geo,
                gprop=''
            )
            
            # Get interest over time
            interest_data = self.pytrends.interest_over_time()
            if not interest_data.empty:
                # Get latest data point
                latest_data = interest_data.iloc[-1].to_dict()
                return {k: v for k, v in latest_data.items() if k != 'isPartial'}
            
            return {}
        except Exception as e:
            print(f"Error fetching interest data: {e}")
            return {}
    
    def get_related_queries(self, keyword: str) -> Dict:
        """Get related queries for a keyword in Kenya"""
        try:
            self.pytrends.build_payload(
                kw_list=[keyword],
                cat=0,
                timeframe='now 7-d',
                geo=self.kenya_geo,
                gprop=''
            )
            
            related_queries = self.pytrends.related_queries()
            return related_queries.get(keyword, {})
        except Exception as e:
            print(f"Error fetching related queries: {e}")
            return {}

class SocialMediaGenerator:
    def __init__(self):
        """Initialize social media post generator"""
        self.post_templates = {
            'trending': [
                "🔥 What's trending in Kenya right now: '{keyword}' is gaining massive attention! {context} #TrendingKenya #Kenya",
                "📈 Kenyans are talking about '{keyword}' - here's what you need to know: {context} #KenyaTrends",
                "🇰🇪 Breaking: '{keyword}' is trending across Kenya! {context} #KenyaNews #Trending",
                "⚡ Hot topic alert: '{keyword}' is the talk of Kenya today! {context} #KenyaTrends #Viral"
            ],
            'educational': [
                "📚 Did you know? '{keyword}' is trending in Kenya. Here's why it matters: {context} #LearnSomethingNew #Kenya",
                "🎓 Trending topic breakdown: '{keyword}' explained for Kenyans {context} #Education #KenyaInsights",
                "💡 Understanding the buzz around '{keyword}' in Kenya: {context} #Knowledge #TrendAnalysis"
            ],
            'engagement': [
                "🤔 What do you think about '{keyword}' trending in Kenya? Share your thoughts! {context} #KenyaDebate",
                "📊 Poll time! How do you feel about '{keyword}' trending in Kenya? {context} #KenyaOpinion #Vote",
                "💬 Let's discuss: '{keyword}' is trending - what's your take, Kenya? {context} #Discussion"
            ]
        }
        
        self.hashtags_kenya = [
            '#Kenya', '#Nairobi', '#KenyaTrends', '#KOT', '#TukoTogether',
            '#KenyaDaily', '#EastAfrica', '#Kenyan', '#NairobiLife', '#KenyaNews'
        ]
    
    def generate_context(self, keyword: str, interest_data: Dict, related_queries: Dict) -> str:
        """Generate contextual information for the post"""
        context_parts = []
        
        # Add interest level context
        if keyword in interest_data:
            interest_level = interest_data[keyword]
            if interest_level > 80:
                context_parts.append("Search interest is at its peak!")
            elif interest_level > 50:
                context_parts.append("Growing rapidly in search trends.")
            else:
                context_parts.append("Gaining momentum in search interest.")
        
        # Add related queries context
        if related_queries.get('top'):
            top_queries = related_queries['top']
            if not top_queries.empty and len(top_queries) > 0:
                related_query = top_queries.iloc[0]['query']
                context_parts.append(f"Related searches include '{related_query}'")
        
        return " ".join(context_parts) if context_parts else "Stay updated with the latest trends!"
    
    def create_social_media_posts(self, trending_keywords: List[str], interest_data: Dict, 
                                related_queries_data: Dict) -> List[Dict]:
        """Create social media posts from trending data"""
        posts = []
        
        for keyword in trending_keywords[:5]:  # Top 5 keywords
            # Generate context
            related_queries = related_queries_data.get(keyword, {})
            context = self.generate_context(keyword, interest_data, related_queries)
            
            # Select random template type
            template_type = random.choice(['trending', 'educational', 'engagement'])
            template = random.choice(self.post_templates[template_type])
            
            # Create post content
            post_content = template.format(keyword=keyword, context=context)
            
            # Add relevant hashtags
            hashtags = random.sample(self.hashtags_kenya, 3)
            post_content += " " + " ".join(hashtags)
            
            # Create post object
            post = {
                'content': post_content,
                'keyword': keyword,
                'template_type': template_type,
                'timestamp': datetime.now().isoformat(),
                'platform': 'multiple',  # Can be adapted for Twitter, Facebook, LinkedIn
                'character_count': len(post_content)
            }
            
            posts.append(post)
        
        return posts

class SocialMediaPlatformAPI:
    """Handle posting to different social media platforms"""
    
    def __init__(self):
        # Add your API keys in .env file
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    def post_to_twitter(self, content: str) -> bool:
        """Post to Twitter using Twitter API v2"""
        # Implement Twitter API v2 posting
        # You'll need to set up Twitter Developer Account
        print(f"[TWITTER] Would post: {content[:100]}...")
        return True
    
    def post_to_facebook(self, content: str) -> bool:
        """Post to Facebook using Graph API"""
        # Implement Facebook Graph API posting
        print(f"[FACEBOOK] Would post: {content[:100]}...")
        return True
    
    def post_to_linkedin(self, content: str) -> bool:
        """Post to LinkedIn using LinkedIn API"""
        # Implement LinkedIn API posting
        print(f"[LINKEDIN] Would post: {content[:100]}...")
        return True

class TrendsAutomationSystem:
    """Main automation system"""
    
    def __init__(self):
        self.trends_fetcher = GoogleTrendsKenya()
        self.post_generator = SocialMediaGenerator()
        self.social_api = SocialMediaPlatformAPI()
        self.data_storage = []
    
    def save_data(self, data: Dict, filename: str = None):
        """Save data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kenya_trends_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_previous_trends(self, filename: str = "previous_trends.json") -> List[str]:
        """Load previously processed trends to avoid duplicates"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('processed_keywords', [])
        except FileNotFoundError:
            return []
    
    def save_processed_trends(self, keywords: List[str], filename: str = "previous_trends.json"):
        """Save processed trends to avoid duplicates"""
        try:
            data = {'processed_keywords': keywords, 'last_updated': datetime.now().isoformat()}
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving processed trends: {e}")
    
    def run_automation(self):
        """Main automation function"""
        print(f"🚀 Starting Kenya Trends automation at {datetime.now()}")
        
        try:
            # Step 1: Fetch trending searches
            print("📊 Fetching trending searches for Kenya...")
            trending_keywords = self.trends_fetcher.get_trending_searches()
            
            if not trending_keywords:
                print("❌ No trending keywords found")
                return
            
            print(f"✅ Found {len(trending_keywords)} trending keywords: {trending_keywords[:3]}...")
            
            # Step 2: Get interest data for keywords
            print("📈 Analyzing interest data...")
            interest_data = self.trends_fetcher.get_interest_over_time(trending_keywords[:5])
            
            # Step 3: Get related queries for context
            print("🔍 Fetching related queries...")
            related_queries_data = {}
            for keyword in trending_keywords[:3]:  # Top 3 for related queries
                related_queries_data[keyword] = self.trends_fetcher.get_related_queries(keyword)
            
            # Step 4: Generate social media posts
            print("✍️ Generating social media posts...")
            posts = self.post_generator.create_social_media_posts(
                trending_keywords, interest_data, related_queries_data
            )
            
            # Step 5: Save data
            automation_data = {
                'timestamp': datetime.now().isoformat(),
                'trending_keywords': trending_keywords,
                'interest_data': interest_data,
                'related_queries': related_queries_data,
                'generated_posts': posts
            }
            
            self.save_data(automation_data)
            
            # Step 6: Display generated posts
            print(f"\n🎉 Generated {len(posts)} social media posts:")
            for i, post in enumerate(posts, 1):
                print(f"\n--- Post {i} ({post['template_type']}) ---")
                print(f"Keyword: {post['keyword']}")
                print(f"Content: {post['content']}")
                print(f"Characters: {post['character_count']}")
                print(f"Platforms: {post['platform']}")
            
            # Step 7: Optionally post to social media (uncomment when ready)
            # for post in posts[:2]:  # Post top 2 posts
            #     self.social_api.post_to_twitter(post['content'])
            #     time.sleep(30)  # Wait between posts
            
            print(f"\n✅ Automation completed successfully at {datetime.now()}")
            
        except Exception as e:
            print(f"❌ Error in automation: {e}")

def setup_scheduler():
    """Setup automated scheduling"""
    automation = TrendsAutomationSystem()
    
    # Schedule automation to run multiple times per day
    schedule.every(6).hours.do(automation.run_automation)  # Every 6 hours
    schedule.every().day.at("09:00").do(automation.run_automation)  # 9 AM daily
    schedule.every().day.at("15:00").do(automation.run_automation)  # 3 PM daily
    schedule.every().day.at("21:00").do(automation.run_automation)  # 9 PM daily
    
    print("⏰ Scheduler set up successfully!")
    print("📅 Automation will run:")
    print("   - Every 6 hours")
    print("   - Daily at 9 AM, 3 PM, and 9 PM (EAT)")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    print("🇰🇪 Google Trends Kenya Social Media Automation System")
    print("=" * 50)
    
    # Choose mode
    mode = input("Choose mode:\n1. Run once\n2. Run with scheduler\nEnter (1 or 2): ").strip()
    
    if mode == "2":
        print("\n🔄 Starting scheduled automation...")
        setup_scheduler()
    else:
        print("\n▶️ Running automation once...")
        automation = TrendsAutomationSystem()
        automation.run_automation()
        print("\n🏁 Single run completed!") 
