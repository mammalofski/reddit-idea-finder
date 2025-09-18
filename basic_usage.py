#!/usr/bin/env python3
"""
Basic Usage Example - Reddit Project Idea Finder

Simplest way to use the Reddit Project Idea Finder Agent to discover
business opportunities with supporting evidence links.
"""

import asyncio
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent


async def find_business_ideas(query):
    """
    Find business ideas based on your query.
    
    Args:
        query (str): What you're looking for (e.g., "AI startup ideas")
        
    Returns:
        str: Analysis with recommendations and Reddit evidence links
    """
    # Create the agent
    agent = RedditProjectIdeaFinderAgent()
    
    # Get the analysis
    result = await agent.find_project_ideas(query)
    
    return result


def main():
    """Simple example usage"""
    
    # Example queries you can try:
    examples = [
        "Find 3 profitable AI startup ideas based on real user problems",
        "What are some micro SaaS opportunities developers are asking for?", 
        "Discover underserved markets in e-commerce",
        "Find pain points in remote work tools",
        "What productivity apps are people desperately wanting?"
    ]
    
    print("🤖 Reddit Project Idea Finder - Basic Usage")
    print("=" * 50)
    print("\nExample queries:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    # Get user input
    query = input(f"\n💡 Enter your query (or number 1-{len(examples)}): ").strip()
    
    # Handle numbered input
    if query.isdigit() and 1 <= int(query) <= len(examples):
        query = examples[int(query) - 1]
        print(f"Using: {query}")
    
    if not query:
        print("❌ No query provided")
        return
    
    print(f"\n🔍 Searching for opportunities...")
    
    # Run the analysis
    try:
        result = asyncio.run(find_business_ideas(query))
        
        print("\n" + "=" * 60)
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        print("\nThe analysis above includes:")
        print("• 📊 Business opportunity evaluations with scores")
        print("• 🔗 Supporting Reddit links organized by category")
        print("• 💡 Specific project recommendations") 
        print("• ⚠️ Risk factors and implementation guidance")
        print("• 📈 Market potential assessments")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("• Reddit API credentials in .env file")
        print("• Google AI API key configured")
        print("• Required packages installed: pip install google-adk praw python-dotenv")


if __name__ == "__main__":
    main()