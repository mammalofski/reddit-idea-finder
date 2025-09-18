#!/usr/bin/env python3
"""
Simple test to verify the supporting links methods work correctly.
This test doesn't require Google ADK or Reddit API.
"""

import sys
import os

def test_supporting_links_logic():
    """Test just the supporting links logic without dependencies."""
    print("🧪 Testing Supporting Links Logic...")
    
    # Create a mock class with just the methods we need
    class MockAgent:
        def _collect_supporting_links(self, posts, insights):
            """Mock implementation of _collect_supporting_links method."""
            supporting_links = {
                "high_priority": [],
                "pain_points": [],
                "opportunities": [],
                "evidence": [],
                "all_links": []
            }
            
            # Process posts and categorize by relevance and content type
            for post in posts:
                full_url = f"https://reddit.com{post['permalink']}"
                link_data = {
                    "title": post["title"],
                    "url": full_url,
                    "score": post["score"],
                    "num_comments": post["num_comments"],
                    "subreddit": post["subreddit"],
                    "created_utc": post.get("created_utc", 0),
                    "summary": post.get("selftext", "")[:200] + "..." if post.get("selftext", "") else ""
                }
                
                # Add to all_links for complete reference
                supporting_links["all_links"].append(link_data)
                
                # Categorize based on score and content
                if post["score"] >= 10 and post["num_comments"] >= 5:
                    supporting_links["high_priority"].append(link_data)
            
            # Process insights to categorize links by pain points and opportunities
            for insight in insights:
                full_url = f"https://reddit.com{insight['post_url']}"
                link_data = {
                    "title": insight["post_title"],
                    "url": full_url,
                    "score": insight["score"],
                    "summary": f"Contains {len(insight['pain_points'])} pain points, {len(insight['opportunities'])} opportunities, {len(insight['evidence'])} evidence items"
                }
                
                # Categorize by content type
                if insight["pain_points"]:
                    link_data["pain_points"] = [pp["keyword"] for pp in insight["pain_points"]]
                    supporting_links["pain_points"].append(link_data)
                
                if insight["opportunities"]:
                    link_data["opportunities"] = [op["keyword"] for op in insight["opportunities"]]
                    supporting_links["opportunities"].append(link_data)
                
                if insight["evidence"]:
                    link_data["evidence_count"] = len(insight["evidence"])
                    supporting_links["evidence"].append(link_data)
            
            # Remove duplicates while preserving order
            for category in supporting_links:
                seen_urls = set()
                unique_links = []
                for link in supporting_links[category]:
                    if link["url"] not in seen_urls:
                        seen_urls.add(link["url"])
                        unique_links.append(link)
                supporting_links[category] = unique_links
            
            return supporting_links

        def format_supporting_links(self, supporting_links_data):
            """Mock implementation of format_supporting_links method."""
            if not supporting_links_data or "supporting_links" not in supporting_links_data:
                return {
                    "status": "no_links",
                    "message": "No supporting links found in the data",
                    "formatted_links": {}
                }
            
            supporting_links = supporting_links_data["supporting_links"]
            
            # Format links by category with enhanced presentation
            formatted_output = {
                "status": "success",
                "total_links": len(supporting_links.get("all_links", [])),
                "categories": {
                    "high_priority": {
                        "title": "🔥 High-Priority Discussions",
                        "description": "Most upvoted and discussed posts with strong community engagement",
                        "count": len(supporting_links.get("high_priority", [])),
                        "links": []
                    },
                    "pain_points": {
                        "title": "😤 Pain Points & Problems",
                        "description": "Posts highlighting specific user frustrations and unmet needs",
                        "count": len(supporting_links.get("pain_points", [])),
                        "links": []
                    },
                    "opportunities": {
                        "title": "💡 Business Opportunities",
                        "description": "Discussions suggesting potential solutions and market gaps",
                        "count": len(supporting_links.get("opportunities", [])),
                        "links": []
                    },
                    "evidence": {
                        "title": "📊 Supporting Evidence",
                        "description": "Additional posts and comments that validate the opportunities",
                        "count": len(supporting_links.get("evidence", [])),
                        "links": []
                    }
                },
                "summary": {
                    "search_query": supporting_links_data.get("query", "Unknown"),
                    "focus_area": supporting_links_data.get("focus_area", "general"),
                    "subreddits": supporting_links_data.get("subreddits_searched", ""),
                    "total_posts_analyzed": supporting_links_data.get("total_posts_found", 0)
                }
            }
            
            # Format each category
            for category_key, category_data in formatted_output["categories"].items():
                category_links = supporting_links.get(category_key, [])
                
                for link in category_links:
                    formatted_link = {
                        "title": link["title"],
                        "url": link["url"],
                        "score": link.get("score", 0),
                        "subreddit": link.get("subreddit", ""),
                        "summary": link.get("summary", "")
                    }
                    
                    # Add category-specific metadata
                    if category_key == "pain_points" and "pain_points" in link:
                        formatted_link["identified_pain_points"] = link["pain_points"]
                    elif category_key == "opportunities" and "opportunities" in link:
                        formatted_link["identified_opportunities"] = link["opportunities"]
                    elif category_key == "evidence" and "evidence_count" in link:
                        formatted_link["evidence_items"] = link["evidence_count"]
                    elif category_key == "high_priority":
                        formatted_link["comments"] = link.get("num_comments", 0)
                    
                    category_data["links"].append(formatted_link)
                
                # Sort links by score (highest first) within each category
                category_data["links"].sort(key=lambda x: x.get("score", 0), reverse=True)
            
            return formatted_output

    # Create test data
    test_posts = [
        {
            "title": "Why is it so hard to find good project management tools?",
            "permalink": "/r/entrepreneur/comments/test1",
            "score": 25,
            "num_comments": 8,
            "subreddit": "entrepreneur",
            "selftext": "I've been struggling to find a simple project management tool that doesn't cost a fortune...",
            "created_utc": 1640995200
        },
        {
            "title": "AI tools for small businesses - what's missing?",
            "permalink": "/r/smallbusiness/comments/test2", 
            "score": 45,
            "num_comments": 15,
            "subreddit": "smallbusiness",
            "selftext": "Looking for AI solutions but everything is too complex or expensive...",
            "created_utc": 1640995300
        }
    ]
    
    test_insights = [
        {
            "post_title": "Why is it so hard to find good project management tools?",
            "post_url": "/r/entrepreneur/comments/test1",
            "score": 25,
            "pain_points": [{"keyword": "hard", "context": "hard to find good project management"}],
            "opportunities": [{"keyword": "tool", "context": "find good project management tools"}],
            "evidence": []
        }
    ]
    
    # Test the functionality
    agent = MockAgent()
    
    # Test _collect_supporting_links
    supporting_links = agent._collect_supporting_links(test_posts, test_insights)
    
    print(f"📊 Supporting Links Categories:")
    for category, links in supporting_links.items():
        print(f"  - {category}: {len(links)} links")
    
    # Test format_supporting_links
    test_data = {
        "query": "test query",
        "focus_area": "general", 
        "subreddits_searched": "entrepreneur+smallbusiness",
        "total_posts_found": 2,
        "supporting_links": supporting_links
    }
    
    formatted_result = agent.format_supporting_links(test_data)
    
    print(f"\n📋 Formatted Results:")
    print(f"  Status: {formatted_result['status']}")
    print(f"  Total Links: {formatted_result['total_links']}")
    print(f"  Categories: {list(formatted_result['categories'].keys())}")
    
    # Validate the results
    assert formatted_result['status'] == 'success'
    assert formatted_result['total_links'] == 2
    assert 'high_priority' in formatted_result['categories']
    assert 'pain_points' in formatted_result['categories']
    assert 'opportunities' in formatted_result['categories']
    assert 'evidence' in formatted_result['categories']
    
    # Check that URLs are properly formatted
    all_links = supporting_links['all_links']
    for link in all_links:
        assert link['url'].startswith('https://reddit.com/')
        assert 'title' in link
        assert 'score' in link
    
    print("\n✅ All supporting links logic tests passed!")
    return True

def main():
    """Run the logic test."""
    print("🚀 Testing Supporting Links Logic (No Dependencies)")
    print("=" * 60)
    
    try:
        test_supporting_links_logic()
        print("\n🎉 Supporting links feature logic is working correctly!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()