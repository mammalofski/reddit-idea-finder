#!/usr/bin/env python3
"""
Enhanced Demo for Reddit Project Idea Finder Agent with Competitive Analysis
Demonstrates the agent's capabilities including Google Search integration
"""

import asyncio
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent

async def main():
    print("🚀 Enhanced Reddit Project Idea Finder Agent - Demo with Competitive Analysis")
    print("="*80)
    
    # Create agent with competitive analysis capabilities
    print("Initializing agent with Google Search integration...")
    agent = RedditProjectIdeaFinderAgent(planner_type="none")  # Using no planner for this demo
    
    # Demo query that will trigger competitive analysis
    demo_query = "Find 2 profitable SaaS ideas for developers and research their competitive landscape"
    
    print(f"\n🎯 Demo Query: {demo_query}")
    print("This will demonstrate:")
    print("✅ Reddit discussion analysis")
    print("✅ Google Search for competitive research") 
    print("✅ Market gap identification")
    print("✅ Feature differentiation opportunities")
    print("✅ Evidence-based recommendations")
    print("-" * 80)
    
    try:
        # Run the enhanced analysis
        result = await agent.find_project_ideas(demo_query)
        
        print("\n" + "="*80)
        print("✅ Enhanced Demo completed successfully!")
        print("The agent has used both Reddit analysis AND Google Search to:")
        print("📊 Identify developer pain points from Reddit")
        print("🔍 Research existing competitive solutions via Google")
        print("💡 Discover market gaps and differentiation opportunities")
        print("📈 Provide evidence-based business recommendations")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("This might be due to:")
        print("- Reddit API credentials not configured")
        print("- Network connectivity issues")
        print("- Google API rate limiting")

if __name__ == "__main__":
    asyncio.run(main())
