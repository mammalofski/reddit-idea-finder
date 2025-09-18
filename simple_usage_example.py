#!/usr/bin/env python3
"""
Simple Usage Example for Reddit Project Idea Finder Agent

This script demonstrates how to use the Reddit Project Idea Finder Agent
in a simple, straightforward way to discover business opportunities with
supporting evidence links from Reddit.

Requirements:
- pip install google-adk praw python-dotenv
- Reddit API credentials in .env file
- Google AI API key in environment
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add src directory to path to import the agent
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent


class SimpleRedditIdeaFinder:
    """
    Simple wrapper for the Reddit Project Idea Finder Agent.
    Makes it easy to use with synchronous Python code.
    """
    
    def __init__(self, model="gemini-2.0-flash"):
        """Initialize the simple wrapper."""
        print("🚀 Initializing Reddit Idea Finder...")
        self.agent = RedditProjectIdeaFinderAgent(model=model)
        print("✅ Ready to find project ideas!")
    
    def find_ideas(self, query, save_results=True):
        """
        Find project ideas based on a query.
        
        Args:
            query (str): What kind of project ideas you're looking for
            save_results (bool): Whether to save results to a JSON file
            
        Returns:
            str: Analysis results with recommendations and evidence links
        """
        print(f"\n🔍 Searching for opportunities: {query}")
        
        # Run the async method
        result = asyncio.run(self.agent.find_project_ideas(query))
        
        # Save results if requested
        if save_results:
            self._save_results(query, result)
        
        return result
    
    def _save_results(self, query, result):
        """Save the results to a timestamped JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"idea_analysis_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "query": query,
            "analysis": result,
            "metadata": {
                "agent_version": "2.0",
                "search_date": datetime.now().isoformat()
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")


def example_ai_startup_ideas():
    """Example: Find AI startup ideas"""
    finder = SimpleRedditIdeaFinder()
    
    query = """Find 3 profitable AI startup ideas based on real user problems. 
    Focus on areas where people are actively complaining about current solutions 
    or requesting features that don't exist yet."""
    
    result = finder.find_ideas(query)
    return result


def example_saas_opportunities():
    """Example: Find micro SaaS opportunities"""
    finder = SimpleRedditIdeaFinder()
    
    query = """What are some micro SaaS opportunities in the developer tools space? 
    Look for small, specific problems that developers mention repeatedly."""
    
    result = finder.find_ideas(query)
    return result


def example_ecommerce_gaps():
    """Example: Find e-commerce market gaps"""
    finder = SimpleRedditIdeaFinder()
    
    query = """Discover underserved markets in e-commerce. Find product categories 
    or services where customers are frustrated with current options."""
    
    result = finder.find_ideas(query)
    return result


def example_remote_work_solutions():
    """Example: Find remote work pain points"""
    finder = SimpleRedditIdeaFinder()
    
    query = """Find pain points in remote work that could become profitable businesses. 
    Look for tools, services, or solutions that remote workers desperately need."""
    
    result = finder.find_ideas(query)
    return result


def run_custom_search():
    """Run a custom search based on user input"""
    print("\n" + "="*60)
    print("🎯 CUSTOM BUSINESS OPPORTUNITY SEARCH")
    print("="*60)
    
    print("\nExamples of good queries:")
    print("• 'Find problems with online learning that could become a startup'")
    print("• 'What developer productivity tools are people asking for?'")
    print("• 'Discover gaps in the fitness app market'")
    print("• 'Find pain points in small business accounting software'")
    
    query = input("\n💡 What business opportunities do you want to discover? ")
    
    if not query.strip():
        print("❌ Please provide a search query.")
        return
    
    finder = SimpleRedditIdeaFinder()
    result = finder.find_ideas(query)
    
    print("\n" + "="*60)
    print("🎉 ANALYSIS COMPLETE!")
    print("="*60)
    print("\nCheck the saved JSON file for detailed results including:")
    print("• Supporting Reddit links organized by category")
    print("• Business opportunity evaluations with scores")
    print("• Implementation recommendations")
    print("• Market analysis and risk factors")


def main():
    """Main function with examples and interactive mode."""
    print("""
🤖 Reddit Project Idea Finder - Simple Usage Examples
====================================================

This tool analyzes Reddit discussions to find profitable business opportunities.
It identifies real user problems and provides supporting evidence links.

Available examples:
1. AI Startup Ideas
2. Micro SaaS Opportunities  
3. E-commerce Market Gaps
4. Remote Work Solutions
5. Custom Search (Interactive)

""")
    
    if len(sys.argv) > 1:
        # Command line mode
        example_num = sys.argv[1]
        
        examples = {
            "1": example_ai_startup_ideas,
            "2": example_saas_opportunities,
            "3": example_ecommerce_gaps,
            "4": example_remote_work_solutions,
            "5": run_custom_search
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"❌ Invalid example number: {example_num}")
            print("Use numbers 1-5")
    else:
        # Interactive mode
        while True:
            try:
                choice = input("Choose an example (1-5) or 'q' to quit: ").strip()
                
                if choice.lower() in ['q', 'quit', 'exit']:
                    print("👋 Thanks for using Reddit Idea Finder!")
                    break
                
                if choice == "1":
                    print("\n🤖 Finding AI startup opportunities...")
                    example_ai_startup_ideas()
                elif choice == "2":
                    print("\n⚡ Finding micro SaaS opportunities...")
                    example_saas_opportunities()
                elif choice == "3":
                    print("\n🛒 Finding e-commerce market gaps...")
                    example_ecommerce_gaps()
                elif choice == "4":
                    print("\n🏠 Finding remote work solutions...")
                    example_remote_work_solutions()
                elif choice == "5":
                    run_custom_search()
                else:
                    print("❌ Please choose a number from 1-5")
                
                print("\n" + "-"*60)
                
            except KeyboardInterrupt:
                print("\n👋 Thanks for using Reddit Idea Finder!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()