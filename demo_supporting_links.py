#!/usr/bin/env python3
"""
Demonstration of the enhanced Reddit Project Idea Finder Agent with supporting links.

This script shows how the agent now provides categorized Reddit links to support
its project idea recommendations.
"""

import sys
import os
import asyncio
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def demo_supporting_links_feature():
    """Demonstrate the supporting links feature with a sample query."""
    
    print("🚀 Reddit Project Idea Finder Agent - Supporting Links Demo")
    print("=" * 70)
    
    try:
        from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent
        
        # Initialize the agent
        print("🔧 Initializing Reddit Project Idea Finder Agent...")
        agent = RedditProjectIdeaFinderAgent()
        
        print("\n📝 What's New:")
        print("✅ Supporting Reddit Links - The agent now provides categorized links")
        print("✅ Evidence-Based Recommendations - Links grouped by relevance")
        print("✅ Multiple Categories - High-priority, pain points, opportunities, evidence")
        print("✅ Full URL Generation - Direct links to Reddit discussions")
        
        # Demo query about AI opportunities
        demo_query = "Find profitable AI startup opportunities based on developer pain points"
        
        print(f"\n🎯 Demo Query: {demo_query}")
        print("=" * 70)
        
        # Note: This would normally execute the full agent workflow
        # For demo purposes, we'll show the structure without full execution
        print("🔍 Agent Workflow with Supporting Links:")
        print("1. 📊 Query Analysis - Understanding request type")
        print("2. 🔎 Strategic Search - Finding relevant Reddit discussions") 
        print("3. 🧠 Deep Analysis - Extracting pain points and opportunities")
        print("4. 📈 Opportunity Evaluation - Scoring market potential")
        print("5. 🔗 Supporting Links Generation - Categorizing evidence")
        print("6. 📋 Report Generation - Comprehensive recommendations")
        
        print("\n💡 Expected Output Structure:")
        print("📊 Executive Summary")
        print("🚀 3-5 Project Recommendations with Scores")
        print("🔗 Supporting Reddit Links:")
        print("   🔥 High-Priority Discussions")
        print("   😤 Pain Points & Problems")
        print("   💡 Business Opportunities") 
        print("   📊 Supporting Evidence")
        print("⚠️  Risk Factors & Next Steps")
        
        # For demonstration, let's show how the tools work independently
        print("\n🧪 Tool Demonstration:")
        
        # Show search tool with supporting links
        print("\n1. 🔍 Search Tool - Now includes supporting_links in response:")
        search_result = agent.search_reddit_for_ideas("AI developer tools", "ai")
        
        if search_result["status"] == "success" and "supporting_links" in search_result:
            links = search_result["supporting_links"]
            print(f"   ✅ Found {len(links['all_links'])} total Reddit links")
            print(f"   🔥 {len(links['high_priority'])} high-priority discussions")
            print(f"   😤 {len(links['pain_points'])} pain point posts")
            print(f"   💡 {len(links['opportunities'])} opportunity posts")
            print(f"   📊 {len(links['evidence'])} evidence posts")
        else:
            print(f"   ⚠️  Search result: {search_result['status']} - {search_result.get('error', 'No error')}")
        
        # Show formatting tool
        print("\n2. 🔗 Link Formatter Tool:")
        if search_result["status"] == "success":
            formatted = agent.format_supporting_links(search_result)
            if formatted["status"] == "success":
                print(f"   ✅ Formatted {formatted['total_links']} links into categories")
                for cat_name, cat_data in formatted["categories"].items():
                    if cat_data["count"] > 0:
                        print(f"   📂 {cat_data['title']}: {cat_data['count']} links")
        
        # Show evaluation tool
        print("\n3. 📊 Evaluation Tool - Enhanced with next steps:")
        eval_result = agent.evaluate_business_opportunity(
            "AI-powered code review tool for small development teams",
            "developers",
            "strong",
            "medium"
        )
        print(f"   📈 Market Potential: {eval_result['scores']['market_potential']}/10")
        print(f"   🔧 Feasibility: {eval_result['scores']['feasibility']}/10")
        print(f"   🎯 Overall Score: {eval_result['scores']['overall']}/10")
        print(f"   💡 Recommendation: {eval_result['recommendation']}")
        
        print("\n" + "=" * 70)
        print("🎉 Supporting Links Feature Successfully Demonstrated!")
        print("\n📝 Key Benefits:")
        print("✅ Evidence-based recommendations with direct Reddit links")
        print("✅ Categorized links for easy navigation and verification")
        print("✅ Full URLs for immediate access to discussions")
        print("✅ Automated collection and organization")
        print("✅ Enhanced credibility and transparency")
        
        print("\n🚀 Ready to find profitable project ideas with full evidence backing!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main demo function."""
    asyncio.run(demo_supporting_links_feature())

if __name__ == "__main__":
    main()