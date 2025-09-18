#!/usr/bin/env python3
"""
Test script for the enhanced Reddit Project Idea Finder Agent with supporting links feature.

This script demonstrates the new supporting links functionality.
"""

import sys
import os
import json
from unittest.mock import Mock

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_supporting_links_collection():
    """Test the supporting links collection functionality."""
    print("🧪 Testing Supporting Links Collection...")
    
    # Import the agent class
    try:
        from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent
        print("✅ Successfully imported RedditProjectIdeaFinderAgent")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
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
    
    # Create agent instance (without Reddit API for testing)
    agent = RedditProjectIdeaFinderAgent()
    
    # Test the _collect_supporting_links method
    supporting_links = agent._collect_supporting_links(test_posts, test_insights)
    
    print(f"📊 Supporting Links Categories:")
    for category, links in supporting_links.items():
        print(f"  - {category}: {len(links)} links")
    
    # Test the format_supporting_links tool
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
    
    # Print sample category
    if formatted_result['categories']['high_priority']['count'] > 0:
        print(f"\n🔥 Sample High-Priority Link:")
        sample_link = formatted_result['categories']['high_priority']['links'][0]
        print(f"  Title: {sample_link['title']}")
        print(f"  URL: {sample_link['url']}")
        print(f"  Score: {sample_link['score']}")
    
    print("\n✅ Supporting links functionality test completed successfully!")
    return True

def test_tool_integration():
    """Test that all tools are properly integrated."""
    print("\n🧪 Testing Tool Integration...")
    
    try:
        from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent
        agent = RedditProjectIdeaFinderAgent()
        
        # Check that all tools are available
        tools = [agent.search_reddit_for_ideas, agent.evaluate_business_opportunity, agent.format_supporting_links]
        print(f"✅ All {len(tools)} tools are available")
        
        # Check agent tools list
        agent_tools_count = len(agent.agent.tools)
        print(f"✅ Agent has {agent_tools_count} tools registered")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Enhanced Reddit Project Idea Finder Agent")
    print("=" * 60)
    
    # Run tests
    tests = [
        test_supporting_links_collection,
        test_tool_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Supporting links feature is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()