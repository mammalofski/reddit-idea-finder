#!/usr/bin/env python3
"""
Evidence Links Example - Reddit Project Idea Finder

This script demonstrates how to extract and work with the supporting 
Reddit evidence links that back up business opportunity discoveries.
"""

import asyncio
import sys
import os
import json
import re
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from reddit_project_idea_finder_agent import RedditProjectIdeaFinderAgent


class EvidenceLinkExtractor:
    """Helper class to extract and format evidence links from agent responses."""
    
    def extract_reddit_links(self, response_text):
        """
        Extract Reddit links from the agent's response text.
        
        Args:
            response_text (str): The full response from the agent
            
        Returns:
            dict: Organized links by category
        """
        # Look for Reddit URLs in the response
        reddit_url_pattern = r'https://reddit\.com/r/[^\s\)]+|https://www\.reddit\.com/r/[^\s\)]+|/r/[a-zA-Z0-9_]+/[^\s\)]+'
        
        urls = re.findall(reddit_url_pattern, response_text)
        
        # Look for categorized sections in the response
        categories = {
            'high_priority': [],
            'pain_points': [],
            'opportunities': [],
            'evidence': [],
            'all_links': urls
        }
        
        # Split response into sections and look for categorized links
        sections = response_text.split('\n')
        current_category = None
        
        for line in sections:
            line = line.strip()
            
            # Detect category headers
            if any(keyword in line.lower() for keyword in ['high-priority', 'high priority']):
                current_category = 'high_priority'
            elif 'pain point' in line.lower():
                current_category = 'pain_points'
            elif 'opportunit' in line.lower():
                current_category = 'opportunities'
            elif 'evidence' in line.lower():
                current_category = 'evidence'
            
            # Extract links from current section
            if current_category and 'reddit.com' in line:
                reddit_urls = re.findall(reddit_url_pattern, line)
                categories[current_category].extend(reddit_urls)
        
        return categories
    
    def save_evidence_links(self, links, query, filename=None):
        """Save evidence links to a structured file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evidence_links_{timestamp}.json"
        
        data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "evidence_links": links,
            "summary": {
                "total_links": len(links.get('all_links', [])),
                "high_priority": len(links.get('high_priority', [])),
                "pain_points": len(links.get('pain_points', [])),
                "opportunities": len(links.get('opportunities', [])),
                "evidence": len(links.get('evidence', []))
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Evidence links saved to: {filename}")
        return filename
    
    def create_markdown_report(self, links, query, filename=None):
        """Create a markdown report of evidence links."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evidence_report_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Evidence Links Report\n\n")
            f.write(f"**Query:** {query}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Summary\n")
            f.write(f"- Total Links Found: {len(links.get('all_links', []))}\n")
            f.write(f"- High Priority Discussions: {len(links.get('high_priority', []))}\n")
            f.write(f"- Pain Points: {len(links.get('pain_points', []))}\n")
            f.write(f"- Opportunities: {len(links.get('opportunities', []))}\n")
            f.write(f"- Supporting Evidence: {len(links.get('evidence', []))}\n\n")
            
            # Write each category
            categories = {
                'high_priority': '🔥 High-Priority Discussions',
                'pain_points': '😤 Pain Points & Problems', 
                'opportunities': '💡 Business Opportunities',
                'evidence': '📊 Supporting Evidence'
            }
            
            for key, title in categories.items():
                if links.get(key):
                    f.write(f"## {title}\n\n")
                    for i, link in enumerate(links[key], 1):
                        f.write(f"{i}. [{link}]({link})\n")
                    f.write("\n")
            
            if links.get('all_links'):
                f.write("## All Links\n\n")
                for i, link in enumerate(links['all_links'], 1):
                    f.write(f"{i}. [{link}]({link})\n")
        
        print(f"📄 Markdown report saved to: {filename}")
        return filename


async def analyze_with_evidence_focus(query):
    """
    Run analysis with special focus on extracting evidence links.
    
    Args:
        query (str): Your business opportunity search query
        
    Returns:
        tuple: (response_text, evidence_links_dict)
    """
    print(f"🔍 Analyzing: {query}")
    print("📊 Focusing on evidence collection...")
    
    # Create agent
    agent = RedditProjectIdeaFinderAgent()
    
    # Enhanced query to emphasize evidence links
    enhanced_query = f"""
    {query}
    
    IMPORTANT: Please provide comprehensive supporting Reddit links organized into clear categories:
    - High-priority discussions (most upvoted/commented)
    - Pain points and problems (specific user frustrations)
    - Business opportunities (market gaps and solutions)
    - Supporting evidence (additional validation)
    
    For each category, include the actual Reddit URLs and brief descriptions.
    """
    
    # Get analysis
    response = await agent.find_project_ideas(enhanced_query)
    
    # Extract evidence links
    extractor = EvidenceLinkExtractor()
    evidence_links = extractor.extract_reddit_links(response)
    
    return response, evidence_links


def main():
    """Main function to demonstrate evidence link extraction."""
    print("🔗 Reddit Evidence Links Extractor")
    print("=" * 50)
    print("\nThis tool finds business opportunities AND extracts")
    print("supporting Reddit evidence links organized by category.")
    
    # Example queries that work well for evidence gathering
    examples = [
        "Find AI automation opportunities that small businesses need",
        "Discover developer productivity tools people are requesting",
        "What e-commerce problems need solving based on merchant complaints?",
        "Find content creation pain points that could become SaaS tools"
    ]
    
    print("\nSuggested queries for rich evidence:")
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
    
    try:
        # Run analysis with evidence focus
        response, evidence_links = asyncio.run(analyze_with_evidence_focus(query))
        
        print("\n" + "=" * 60)
        print("🎉 ANALYSIS COMPLETE WITH EVIDENCE!")
        print("=" * 60)
        
        # Display evidence summary
        print(f"\n📊 Evidence Links Summary:")
        print(f"• Total Reddit links found: {len(evidence_links.get('all_links', []))}")
        print(f"• High-priority discussions: {len(evidence_links.get('high_priority', []))}")
        print(f"• Pain points identified: {len(evidence_links.get('pain_points', []))}")
        print(f"• Business opportunities: {len(evidence_links.get('opportunities', []))}")
        print(f"• Supporting evidence: {len(evidence_links.get('evidence', []))}")
        
        # Save evidence links
        extractor = EvidenceLinkExtractor()
        json_file = extractor.save_evidence_links(evidence_links, query)
        md_file = extractor.create_markdown_report(evidence_links, query)
        
        print(f"\n📁 Files created:")
        print(f"• {json_file} (structured data)")
        print(f"• {md_file} (readable report)")
        
        # Show a few example links
        if evidence_links.get('all_links'):
            print(f"\n🔗 Sample evidence links:")
            for i, link in enumerate(evidence_links['all_links'][:3], 1):
                print(f"{i}. {link}")
            
            if len(evidence_links['all_links']) > 3:
                print(f"... and {len(evidence_links['all_links']) - 3} more links")
        
        print(f"\n✅ Check the generated files for complete evidence collection!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("• Reddit API credentials in .env file")
        print("• Google AI API key configured")
        print("• Required packages: pip install google-adk praw python-dotenv")


if __name__ == "__main__":
    main()