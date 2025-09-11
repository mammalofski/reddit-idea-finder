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
    
    def search_posts(self, query, subreddit_name="all", sort="relevance", time_filter="all", limit=25, 
                     include_comments=False, max_comments=5, comment_limit_more=2):
        """
        Search Reddit posts using PRAW with optional comment fetching
        
        Args:
            query (str): Search query (e.g., "saas ideas")
            subreddit_name (str): Subreddit to search in (default: "all")
            sort (str): Sort method - "relevance", "hot", "top", "new", "comments"
            time_filter (str): Time filter - "all", "day", "hour", "month", "week", "year"
            limit (int): Number of results to return (default: 25)
            include_comments (bool): Whether to fetch comments for each post (default: False)
            max_comments (int): Maximum number of comments to fetch per post (0 for all)
            comment_limit_more (int): Limit for MoreComments replacement (default: 2)
        
        Returns:
            list: List of dictionaries containing post information with optional comments
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
                    'id': submission.id,
                    'comments': []  # Initialize empty comments list
                }
                
                # Fetch comments if requested
                if include_comments:
                    print(f"Fetching comments for: {submission.title[:50]}...")
                    post_data['comments'] = self.fetch_post_comments(
                        submission, max_comments, comment_limit_more
                    )
                
                posts.append(post_data)
            
            return posts
        
        except Exception as e:
            print(f"Error searching Reddit: {e}")
            return []
    
    def fetch_post_comments(self, submission, max_comments=10, limit_more=5):
        """
        Fetch comments for a specific Reddit post submission
        
        Args:
            submission: PRAW submission object
            max_comments (int): Maximum number of comments to return (0 for all)
            limit_more (int): Limit for MoreComments replacement (0 to remove all, None for all)
        
        Returns:
            list: List of comment dictionaries
        """
        try:
            # Replace MoreComments objects with actual comments
            # limit=5 means replace up to 5 "load more comments" sections
            # This balances between getting enough comments and API rate limits
            submission.comments.replace_more(limit=limit_more)
            
            # Get all comments as a flat list
            all_comments = submission.comments.list()
            
            comments_data = []
            for i, comment in enumerate(all_comments):
                if max_comments > 0 and i >= max_comments:
                    break
                    
                comment_data = {
                    'id': comment.id,
                    'body': comment.body,
                    'author': str(comment.author) if comment.author else '[deleted]',
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'parent_id': comment.parent_id,
                    'is_submitter': comment.is_submitter,
                    'depth': getattr(comment, 'depth', 0),
                    'permalink': f"https://reddit.com{comment.permalink}"
                }
                comments_data.append(comment_data)
            
            return comments_data
        
        except Exception as e:
            print(f"  Error fetching comments: {e}")
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
    
    def search_and_save(self, queries, filename="reddit_search_results.json", include_comments=False, max_comments=5):
        """Search for multiple queries and save results to a JSON file"""
        all_results = {}
        
        for query in queries:
            print(f"Searching for: '{query}'...")
            results = self.search_posts(
                query=query,
                subreddit_name="entrepreneur+startups+SaaS+business+sideproject",
                sort="top",
                time_filter="month",
                limit=15,
                include_comments=include_comments,
                max_comments=max_comments
            )
            all_results[query] = results
            print(f"Found {len(results)} posts for '{query}'")
        
        # Save to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\nResults saved to {filename}")
        return all_results
    
    def quick_idea_search(self, idea_type="saas", include_comments=False, max_comments=3):
        """Quick search for different types of business ideas"""
        search_terms = {
            "saas": "saas ideas OR micro saas OR software ideas",
            "ecommerce": "ecommerce ideas OR online store ideas",
            "service": "service business ideas OR consulting ideas",
            "app": "app ideas OR mobile app startup",
            "ai": "ai startup ideas OR machine learning business"
        }
        
        query = search_terms.get(idea_type.lower(), idea_type)
        return self.search_posts(query, "entrepreneur+startups+business", limit=20, 
                                include_comments=include_comments, max_comments=max_comments)
    
    def display_posts(self, posts, title="Search Results", show_comments=True):
        """Display posts in a formatted way with optional comments"""
        print(f"\n{title}")
        print("="*80)
        
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Author: u/{post['author']} | Subreddit: r/{post['subreddit']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']} | Date: {post['created_utc'].strftime('%Y-%m-%d')}")
            if post['selftext']:
                print(f"   Text: {post['selftext']}")
            print(f"   Link: {post['permalink']}")
            
            # Display comments if available and requested
            if show_comments and 'comments' in post and post['comments']:
                print(f"\n   💬 TOP COMMENTS ({len(post['comments'])} fetched):")
                for j, comment in enumerate(post['comments'][:3], 1):  # Show top 3 comments
                    print(f"      {j}. u/{comment['author']} (Score: {comment['score']})")
                    comment_text = comment['body'][:100] + "..." if len(comment['body']) > 100 else comment['body']
                    print(f"         {comment_text}")
                if len(post['comments']) > 3:
                    print(f"         ... and {len(post['comments']) - 3} more comments")
            elif show_comments and 'comments' in post:
                print(f"   💬 No comments fetched")
            
            print("-" * 60)


def main():
    """Main function demonstrating the Reddit Idea Finder with comment fetching"""
    finder = RedditIdeaFinder()
    
    # Example 1: Search for SaaS ideas (without comments for speed)
    print("🔍 Searching for SaaS ideas...")
    saas_posts = finder.search_posts(
        query="saas ideas",
        subreddit_name="entrepreneur+startups+SaaS",
        sort="relevance",
        time_filter="month",
        limit=5,  # Reduced for demo
        include_comments=False
    )
    
    finder.display_posts(saas_posts, "SaaS Ideas from Reddit", show_comments=False)
    
    # Example 2: Search with comments (smaller sample)
    print("\n🔍 Searching for micro SaaS ideas WITH COMMENTS...")
    micro_saas_posts = finder.search_posts(
        query="micro saas",
        subreddit_name="SaaS",
        sort="top",
        time_filter="month",
        limit=2,  # Small sample to avoid rate limits
        include_comments=True,
        max_comments=3,
        comment_limit_more=1
    )
    
    finder.display_posts(micro_saas_posts, "Micro SaaS Ideas with Comments", show_comments=True)
    
    # Example 3: Analyze results
    print(finder.analyze_results(saas_posts))
    
    # Example 4: Filter high-quality posts
    high_quality = finder.filter_high_quality_posts(saas_posts, min_score=5, min_comments=10)
    finder.display_posts(high_quality, "High Quality Posts", show_comments=False)
    
    # Example 5: Quick search for different idea types WITH comments
    print("\n🚀 Quick AI Startup Ideas Search with Comments...")
    ai_posts = finder.quick_idea_search("ai", include_comments=True, max_comments=2)
    finder.display_posts(ai_posts[:2], "AI Startup Ideas (Top 2 with Comments)", show_comments=True)
    
    # Example 6: Search and save multiple queries with comments
    print("\n💾 Searching and saving multiple queries with comments...")
    idea_queries = [
        "profitable saas ideas",
        "micro saas 2024"
    ]
    
    # Uncomment the line below to run the search and save with comments
    # results = finder.search_and_save(idea_queries, "idea_search_results_with_comments.json", 
    #                                 include_comments=True, max_comments=3)
    print("Search and save example ready (uncomment to run with comments)")
    
    print("\n✅ Demo completed! Comments are now integrated into all search functions.")
    print("💡 Use include_comments=True in any search method to fetch comments.")
    print("⚡ Adjust max_comments and comment_limit_more to control API usage.")


if __name__ == "__main__":
    main()
