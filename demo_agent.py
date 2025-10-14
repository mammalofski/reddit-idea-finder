#!/usr/bin/env python3
"""
Demo script for Reddit Project Idea Finder Agent without requiring actual Reddit credentials.
Shows the agent structure and how it would work with mock data.
"""

import asyncio
import sys
import os

# Add the src directory to path
sys.path.append('/home/mammalofski/projects/idea_finder_agent/src')

try:
    from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent
    
    async def demo_agent():
        print("🚀 Reddit Project Idea Finder Agent - Demo Mode")
        print("=" * 60)
        
        try:
            # Create the agent
            agent = RedditProjectIdeaFinderAgent()
            
            # Test query
            query = "find small profitable projects to sell entertainment for the rich. look for complains or suggestions."
            print(f"\n🎯 Demo Query: {query}")
            
            # Run the agent
            result = await agent.find_project_ideas(query)
            # result = await agent.run_interactive_session()
            
            print("\n✅ Demo completed successfully!")
            print(result)
            
        except Exception as e:
            print(f"⚠️ Demo running in limited mode due to: {e}")
            print("\nTo run with full functionality:")
            print("1. Copy .env.template to .env")
            print("2. Add your Reddit API credentials")
            print("3. Run: python src/reddit_project_idea_finder_agent.py")
            
            # Show the agent structure anyway
            print("\n📋 Agent Architecture Overview:")
            print("✓ Google ADK integration")
            print("✓ Reddit search tool")
            print("✓ Opportunity evaluation tool")
            print("✓ Recursive search capabilities")
            print("✓ Evidence-based reasoning")
            print("✓ Interactive CLI interface")
    
    if __name__ == "__main__":
        asyncio.run(demo_agent())
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed the required packages:")
    print("pip install google-adk praw python-dotenv")
