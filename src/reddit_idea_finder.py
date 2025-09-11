#!/usr/bin/env python3
"""
Reddit Idea Finder - Search Reddit for business and SaaS ideas using PRAW
Requirements: pip install praw python-dotenv
"""

import praw
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedditIdeaFinder:
    def __init__(self):
        """Initialize Reddit API client"""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_SECRET'),
            user_agent='idea_finder_agent:v1.0 (by u/your_username)',  # Change this to your username
        )
        print(f"Reddit instance created. Read-only mode: {self.reddit.read_only}")
    
    def search_posts(self, query, subreddit_name="all", sort="relevance", time_filter="all", limit=25):
        """
        Search Reddit posts using PRAW
        
        Args:
            query (str): Search query (e.g., "saas ideas")
            subreddit_name (str): Subreddit to search in (default: "all")
            sort (str): Sort method - "relevance", "hot", "top", "new", "comments"
            time_filter (str): Time filter - "all", "day", "hour", "month", "week", "year"
            limit (int): Number of results to return (default: 25)
        
        Returns:
            list: List of dictionaries containing post information
        """
        try:
            # Get the subreddit
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Search for posts
            search_results = subreddit.search(
                query=query,
                sort=sort,
                time_filter=time_filter,
                limit=limit
            )
            
            posts = []
            for submission in search_results:
                post_data = {
                    'title': submission.title,
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'created_utc': datetime.fromtimestamp(submission.created_utc),
                    'subreddit': str(submission.subreddit),
                    'url': submission.url,
                    'permalink': f"https://reddit.com{submission.permalink}",
                    'selftext': submission.selftext[:300] + "..." if len(submission.selftext) > 300 else submission.selftext,
                    'is_self': submission.is_self,
                    'id': submission.id
                }
                posts.append(post_data)
            
            return posts
        
        except Exception as e:
            print(f"Error searching Reddit: {e}")
            return []
    
    def filter_high_quality_posts(self, posts, min_score=5, min_comments=2):
        """Filter posts based on engagement metrics"""
        return [post for post in posts if post['score'] >= min_score and post['num_comments'] >= min_comments]
    
    def analyze_results(self, posts):
        """Analyze search results and provide insights"""
        if not posts:
            return "No posts to analyze"
        
        total_posts = len(posts)
        avg_score = sum(post['score'] for post in posts) / total_posts
        avg_comments = sum(post['num_comments'] for post in posts) / total_posts
        
        # Top subreddits
        subreddit_counts = {}
        for post in posts:
            subreddit = post['subreddit']
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        analysis = f"""
📊 SEARCH RESULTS ANALYSIS
{'='*50}
Total posts found: {total_posts}
Average score: {avg_score:.1f}
Average comments: {avg_comments:.1f}

📍 Top Subreddits:"""
        
        for subreddit, count in top_subreddits:
            analysis += f"\n    r/{subreddit}: {count} posts"
        
        return analysis
    
    def search_and_save(self, queries, filename="reddit_search_results.json"):
        """Search for multiple queries and save results to a JSON file"""
        all_results = {}
        
        for query in queries:
            print(f"Searching for: '{query}'...")
            results = self.search_posts(
                query=query,
                subreddit_name="entrepreneur+startups+SaaS+business+sideproject",
                sort="top",
                time_filter="month",
                limit=15
            )
            all_results[query] = results
            print(f"Found {len(results)} posts for '{query}'")
        
        # Save to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\nResults saved to {filename}")
        return all_results
    
    def quick_idea_search(self, idea_type="saas"):
        """Quick search for different types of business ideas"""
        search_terms = {
            "saas": "saas ideas OR micro saas OR software ideas",
            "ecommerce": "ecommerce ideas OR online store ideas",
            "service": "service business ideas OR consulting ideas",
            "app": "app ideas OR mobile app startup",
            "ai": "ai startup ideas OR machine learning business"
        }
        
        query = search_terms.get(idea_type.lower(), idea_type)
        return self.search_posts(query, "entrepreneur+startups+business", limit=20)
    
    def display_posts(self, posts, title="Search Results"):
        """Display posts in a formatted way"""
        print(f"\n{title}")
        print("="*80)
        
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Author: u/{post['author']} | Subreddit: r/{post['subreddit']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']} | Date: {post['created_utc'].strftime('%Y-%m-%d')}")
            if post['selftext']:
                print(f"   Text: {post['selftext']}")
            print(f"   Link: {post['permalink']}")
            print("-" * 60)


def main():
    """Main function demonstrating the Reddit Idea Finder"""
    finder = RedditIdeaFinder()
    
    # Example 1: Search for SaaS ideas
    print("🔍 Searching for SaaS ideas...")
    saas_posts = finder.search_posts(
        query="saas ideas",
        subreddit_name="entrepreneur+startups+SaaS",
        sort="relevance",
        time_filter="month",
        limit=10
    )
    
    finder.display_posts(saas_posts, "SaaS Ideas from Reddit")
    
    # Example 2: Analyze results
    print(finder.analyze_results(saas_posts))
    
    # Example 3: Filter high-quality posts
    high_quality = finder.filter_high_quality_posts(saas_posts, min_score=8, min_comments=15)
    finder.display_posts(high_quality, "High Quality Posts")
    
    # Example 4: Quick search for different idea types
    print("\n🚀 Quick AI Startup Ideas Search...")
    ai_posts = finder.quick_idea_search("ai")
    finder.display_posts(ai_posts[:5], "AI Startup Ideas (Top 5)")
    
    # Example 5: Search and save multiple queries
    print("\n💾 Searching and saving multiple queries...")
    idea_queries = [
        "saas ideas",
        "startup ideas 2024",
        "micro saas",
        "profitable business ideas"
    ]
    
    # Uncomment the line below to run the search and save
    # results = finder.search_and_save(idea_queries, "idea_search_results.json")
    print("Search and save example ready (uncomment to run)")


if __name__ == "__main__":
    main()
