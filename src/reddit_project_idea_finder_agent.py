#!/usr/bin/env python3
"""
Reddit Project Idea Finder Agent - Intelligent business opportunity discovery using Google ADK

This agent analyzes Reddit discussions to identify profitable project opportunities
by finding user pain points, unmet needs, and market gaps.

Requirements: 
- pip install google-adk praw python-dotenv
- Reddit API credentials in .env file
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any

# Google ADK imports
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Add current directory to path for importing reddit_idea_finder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from reddit_idea_finder import RedditIdeaFinder
    REDDIT_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: reddit_idea_finder.py not found. Reddit functionality will be limited.")
    REDDIT_AVAILABLE = False

class RedditProjectIdeaFinderAgent:
    """
    Intelligent agent for discovering profitable project opportunities from Reddit discussions.
    
    Uses Google ADK to orchestrate sophisticated analysis of Reddit content, identifying
    pain points, market gaps, and business opportunities with evidence-based reasoning.
    """
    
    def __init__(self, model="gemini-2.5-flash"):
        """
        Initialize the Reddit Project Idea Finder Agent.
        
        Args:
            model (str): Model to use for the agent (default: gemini-2.0-flash)
        """
        self.model = model
        self.reddit_finder = None
        self._initialize_reddit()
        self._setup_tools()
        self._create_agent()
        self._setup_session()
        
    def _initialize_reddit(self):
        """Initialize Reddit API connection if available."""
        if REDDIT_AVAILABLE:
            try:
                self.reddit_finder = RedditIdeaFinder()
                print("✅ Reddit API connection established")
            except Exception as e:
                print(f"❌ Reddit API connection failed: {e}")
                print("Make sure you have REDDIT_CLIENT_ID and REDDIT_SECRET in your .env file")
                self.reddit_finder = None
        
    def _setup_tools(self):
        """Set up the agent's tools for Reddit analysis and opportunity evaluation."""
        
        def search_reddit_for_ideas(query: str, focus_area: str = "general") -> Dict[str, Any]:
            """
            Tool function that searches Reddit for project ideas and pain points.
            
            Args:
                query (str): Search query for finding ideas (e.g., "saas problems", "startup pain points")
                focus_area (str): Area to focus on (e.g., "ai", "saas", "ecommerce", "developer")
            
            Returns:
                dict: Structured results with posts, analysis, and insights
            """
            print(f"🔍 Searching Reddit for ideas: '{query}' in focus area: '{focus_area}'")
            
            if not self.reddit_finder:
                return {
                    "status": "error",
                    "error": "Reddit API not available. Check credentials.",
                    "posts": [],
                    "insights": [],
                    "supporting_links": {}
                }
            
            try:
                # Determine subreddits based on focus area
                subreddit_map = {
                    "ai": "MachineLearning+artificial+ArtificialIntelligence+LocalLLaMA",
                    "saas": "SaaS+entrepreneur+startups+microsaas",
                    "ecommerce": "ecommerce+shopify+entrepreneur+dropship",
                    "developer": "webdev+programming+softwaregore+ProgrammerHumor",
                    "general": "entrepreneur+startups+business+SideProject+solopreneur"
                }
                
                target_subreddits = subreddit_map.get(focus_area, subreddit_map["general"])
                
                # Search for posts with comments for deeper insights
                posts = self.reddit_finder.search_posts(
                    query=query,
                    subreddit_name=target_subreddits,
                    sort="top",
                    time_filter="month",
                    limit=10,
                    include_comments=True,
                    max_comments=5
                )
                
                # Filter for high-quality posts
                quality_posts = self.reddit_finder.filter_high_quality_posts(posts, min_score=3, min_comments=2)
                
                # Extract pain points and opportunities
                insights = self._extract_pain_points(quality_posts)
                
                # Collect supporting Reddit links
                supporting_links = self._collect_supporting_links(quality_posts, insights)
                
                return {
                    "status": "success",
                    "query": query,
                    "focus_area": focus_area,
                    "subreddits_searched": target_subreddits,
                    "total_posts_found": len(posts),
                    "quality_posts": len(quality_posts),
                    "posts": quality_posts[:5],  # Return top 5 for analysis
                    "insights": insights,
                    "supporting_links": supporting_links
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Search failed: {str(e)}",
                    "posts": [],
                    "insights": [],
                    "supporting_links": {}
                }
        
        def evaluate_business_opportunity(
            problem_description: str, 
            target_market: str, 
            evidence_strength: str = "medium",
            implementation_complexity: str = "medium"
        ) -> Dict[str, Any]:
            """
            Tool to evaluate the business potential of a discovered opportunity.
            
            Args:
                problem_description (str): Description of the problem/pain point identified
                target_market (str): Target market or user segment (e.g., "developers", "small businesses")
                evidence_strength (str): Strength of evidence from Reddit ("weak", "medium", "strong")
                implementation_complexity (str): Technical complexity ("low", "medium", "high")
            
            Returns:
                dict: Detailed evaluation with scores and recommendations
            """
            print(f"📊 Evaluating opportunity: {problem_description[:50]}...")
            
            # Market size estimates (simplified scoring)
            market_scores = {
                "developers": 8, "small businesses": 9, "startups": 7, "enterprise": 6,
                "consumers": 9, "students": 5, "freelancers": 6, "content creators": 7,
                "ecommerce": 8, "saas companies": 7
            }
            
            # Evidence strength multipliers
            evidence_multipliers = {"weak": 0.6, "medium": 1.0, "strong": 1.4}
            
            # Implementation complexity factors
            complexity_factors = {
                "low": {"time_to_market": 1.3, "resource_requirement": 0.7},
                "medium": {"time_to_market": 1.0, "resource_requirement": 1.0},
                "high": {"time_to_market": 0.7, "resource_requirement": 1.5}
            }
            
            # Calculate base market score
            market_score = 5  # default
            for market, score in market_scores.items():
                if market.lower() in target_market.lower():
                    market_score = max(market_score, score)
            
            # Apply evidence strength and complexity factors
            evidence_score = market_score * evidence_multipliers.get(evidence_strength, 1.0)
            complexity_factor = complexity_factors.get(implementation_complexity, complexity_factors["medium"])
            
            # Calculate final scores
            market_potential = min(10, evidence_score)
            feasibility_score = min(10, (complexity_factor["time_to_market"] * 5) + (1/complexity_factor["resource_requirement"] * 5))
            overall_score = (market_potential * 0.6) + (feasibility_score * 0.4)
            
            # Generate recommendation
            if overall_score >= 8:
                recommendation = "🚀 HIGH PRIORITY - Strong opportunity with good market potential"
            elif overall_score >= 6:
                recommendation = "⚡ MEDIUM PRIORITY - Solid opportunity worth exploring"
            elif overall_score >= 4:
                recommendation = "💡 LOW PRIORITY - Interesting but challenging opportunity"
            else:
                recommendation = "⚠️ SKIP - Low potential or high risk"
            
            # Monetization suggestions
            monetization_strategies = []
            if "developer" in target_market.lower():
                monetization_strategies.extend(["SaaS subscription", "Usage-based pricing", "Enterprise licenses"])
            if "small business" in target_market.lower():
                monetization_strategies.extend(["Monthly subscription", "Freemium model", "Per-seat pricing"])
            if "consumer" in target_market.lower():
                monetization_strategies.extend(["Freemium", "In-app purchases", "Advertising"])
            
            return {
                "problem": problem_description,
                "target_market": target_market,
                "scores": {
                    "market_potential": round(market_potential, 1),
                    "feasibility": round(feasibility_score, 1),
                    "overall": round(overall_score, 1)
                },
                "recommendation": recommendation,
                "monetization_strategies": monetization_strategies,
                "risk_factors": self._get_risk_factors(implementation_complexity, evidence_strength),
                "next_steps": self._get_next_steps(overall_score)
            }
        
        def format_supporting_links(supporting_links_data: Dict[str, Any]) -> Dict[str, Any]:
            """
            Tool to format supporting Reddit links into a structured, presentable format.
            
            Args:
                supporting_links_data (dict): Raw supporting links data from search results
                
            Returns:
                dict: Formatted and categorized supporting links for presentation
            """
            print("🔗 Formatting supporting Reddit links...")
            
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
        
        # Store tools as instance methods
        self.search_reddit_for_ideas = search_reddit_for_ideas
        self.evaluate_business_opportunity = evaluate_business_opportunity
        self.format_supporting_links = format_supporting_links
    
    def _extract_pain_points(self, posts: List[Dict]) -> List[Dict[str, Any]]:
        """Extract pain points and opportunities from Reddit posts."""
        insights = []
        
        # Keywords that indicate problems/pain points
        pain_keywords = [
            "frustrating", "annoying", "hate", "terrible", "awful", "sucks",
            "problem", "issue", "struggle", "difficult", "hard", "painful",
            "missing", "lack", "need", "wish", "want", "should have",
            "broken", "buggy", "slow", "expensive", "overpriced"
        ]
        
        # Keywords that indicate opportunities
        opportunity_keywords = [
            "idea", "startup", "business", "opportunity", "gap", "market",
            "solution", "tool", "app", "platform", "service", "product",
            "feature request", "would pay for", "take my money"
        ]
        
        for post in posts:
            post_insight = {
                "post_title": post["title"],
                "post_url": post["permalink"],
                "score": post["score"],
                "pain_points": [],
                "opportunities": [],
                "evidence": []
            }
            
            # Analyze post content
            content = (post.get("selftext", "") + " " + post["title"]).lower()
            
            # Check for pain indicators
            for keyword in pain_keywords:
                if keyword in content:
                    post_insight["pain_points"].append({
                        "keyword": keyword,
                        "context": content[max(0, content.find(keyword)-50):content.find(keyword)+50]
                    })
            
            # Check for opportunity indicators  
            for keyword in opportunity_keywords:
                if keyword in content:
                    post_insight["opportunities"].append({
                        "keyword": keyword,
                        "context": content[max(0, content.find(keyword)-50):content.find(keyword)+50]
                    })
            
            # Analyze comments for additional insights
            for comment in post.get("comments", []):
                comment_text = comment["body"].lower()
                
                # Look for high-scoring comments with pain points
                if comment["score"] > 2:
                    for keyword in pain_keywords + opportunity_keywords:
                        if keyword in comment_text:
                            post_insight["evidence"].append({
                                "type": "comment",
                                "author": comment["author"],
                                "score": comment["score"],
                                "keyword": keyword,
                                "text": comment["body"][:200] + "..." if len(comment["body"]) > 200 else comment["body"]
                            })
            
            # Only include posts with interesting insights
            if post_insight["pain_points"] or post_insight["opportunities"] or post_insight["evidence"]:
                insights.append(post_insight)
        
        return insights
    
    def _collect_supporting_links(self, posts: List[Dict], insights: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Collect and categorize supporting Reddit links from discovered posts and insights.
        
        Args:
            posts: List of Reddit posts from the search
            insights: List of extracted insights with pain points and opportunities
            
        Returns:
            dict: Categorized supporting links with metadata
        """
        supporting_links = {
            "high_priority": [],  # Posts with strong evidence and high scores
            "pain_points": [],    # Posts highlighting specific problems
            "opportunities": [],  # Posts suggesting business opportunities
            "evidence": [],       # Additional supporting evidence
            "all_links": []       # Complete list for reference
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
    
    def _get_risk_factors(self, complexity: str, evidence: str) -> List[str]:
        """Generate risk factors based on complexity and evidence."""
        risks = []
        
        if complexity == "high":
            risks.extend([
                "High development costs and time",
                "Technical complexity may lead to delays",
                "Requires significant expertise"
            ])
        
        if evidence == "weak":
            risks.extend([
                "Limited market validation",
                "Uncertainty about real demand"
            ])
        
        if complexity == "low" and evidence == "strong":
            risks.append("Market may be competitive due to low barriers")
        
        return risks
    
    def _get_next_steps(self, score: float) -> List[str]:
        """Generate recommended next steps based on opportunity score."""
        if score >= 8:
            return [
                "Create detailed market research plan",
                "Build MVP or prototype",
                "Validate with potential customers",
                "Analyze competition thoroughly"
            ]
        elif score >= 6:
            return [
                "Conduct deeper Reddit analysis",
                "Survey potential users",
                "Research existing solutions",
                "Create basic concept validation"
            ]
        elif score >= 4:
            return [
                "Monitor the space for developments",
                "Consider alternative approaches",
                "Look for adjacent opportunities"
            ]
        else:
            return [
                "Archive for future reference",
                "Focus on higher-potential opportunities"
            ]
    
    def _create_agent(self):
        """Create the main Reddit Project Idea Finder Agent."""
        self.agent = Agent(
            name="reddit_project_idea_finder",
            model=self.model,
            description="An intelligent agent that discovers profitable project opportunities by analyzing Reddit discussions. Identifies user pain points, unmet needs, and market gaps to suggest viable project ideas.",
            instruction="""You are a sophisticated business opportunity analyst specializing in discovering profitable project ideas from Reddit discussions.

Your process:
1. **Query Analysis**: Interpret user requests to understand what type of opportunities they're seeking
2. **Strategic Search**: Use search_reddit_for_ideas to find relevant discussions about problems, pain points, and unmet needs
3. **Deep Analysis**: Examine posts and comments to identify patterns of user frustration and desired solutions
4. **Opportunity Evaluation**: Use evaluate_business_opportunity to assess market potential and feasibility
5. **Supporting Links Generation**: Use format_supporting_links to provide categorized Reddit links that back up your findings
6. **Recursive Investigation**: If initial findings suggest promising areas, conduct follow-up searches for deeper insights
7. **Report Generation**: Provide 3-5 well-researched project recommendations with clear reasoning and supporting links

Guidelines:
- Focus on real problems people are actively discussing
- Look for recurring complaints and feature requests
- Prioritize opportunities with strong evidence and market potential
- Consider implementation complexity and time-to-market
- Provide specific, actionable recommendations
- Always include supporting evidence from Reddit discussions
- Generate and present categorized supporting Reddit links for each search conducted
- Format supporting links to show high-priority discussions, pain points, opportunities, and evidence separately

Output Format:
For each analysis, always provide:
1. Executive summary of findings
2. 3-5 specific project recommendations with evaluation scores
3. Categorized supporting Reddit links organized by relevance and content type
4. Risk factors and next steps for each opportunity

You should be thorough but efficient, conducting multiple searches when needed to build a comprehensive understanding of opportunities.""",
            tools=[self.search_reddit_for_ideas, self.evaluate_business_opportunity, self.format_supporting_links]
        )
        
        print(f"✅ Reddit Project Idea Finder Agent created: '{self.agent.name}'")
        print(f"Model: {self.agent.model}")
        print(f"Tools available: {len(self.agent.tools)}")
    
    def _setup_session(self):
        """Set up session management for the agent."""
        self.session_service = InMemorySessionService()
        self.app_name = "reddit_idea_finder_app"
        self.user_id = "analyst_1"
        self.session_id = "idea_session_001"
        
        # Create runner
        self.runner = Runner(
            agent=self.agent,
            app_name=self.app_name,
            session_service=self.session_service
        )
        
        print(f"🚀 Reddit Idea Finder Agent setup complete!")
    
    async def find_project_ideas(self, query: str) -> str:
        """
        Interact with the Reddit Project Idea Finder Agent to discover opportunities.
        
        Args:
            query (str): User's request for project ideas
            
        Returns:
            str: Agent's analysis and recommendations
        """
        print(f"\n🎯 User Query: {query}")
        
        # Create session if not exists
        try:
            session = await self.session_service.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=self.session_id
            )
        except Exception:
            # Session might already exist
            pass
        
        # Prepare the user's message
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        final_response = "No response received from agent."
        
        # Execute the agent and collect the response
        async for event in self.runner.run_async(
            user_id=self.user_id, 
            session_id=self.session_id, 
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response = f"Agent escalated: {event.error_message or 'Unknown error'}"
                break
        
        print(f"\n📊 Agent Analysis Complete")
        print("="*80)
        print(final_response)
        print("="*80)
        
        return final_response
    
    def run_interactive_session(self):
        """Run an interactive session where users can ask for project ideas."""
        print("""
🤖 Reddit Project Idea Finder Agent - Interactive Mode
=====================================================

Ask me to find profitable project opportunities from Reddit discussions!

Examples:
- "Find 3 profitable AI startup ideas based on real user problems"
- "What are some micro SaaS opportunities in the developer tools space?"
- "Discover underserved markets in e-commerce"
- "Find pain points in remote work that could become profitable businesses"

Type 'quit' to exit.
""")
        
        async def interactive_loop():
            while True:
                try:
                    query = input("\n💡 What opportunities are you looking for? ")
                    
                    if query.lower() in ['quit', 'exit', 'q']:
                        print("👋 Thanks for using Reddit Project Idea Finder Agent!")
                        break
                    
                    if not query.strip():
                        continue
                    
                    await self.find_project_ideas(query)
                    
                except KeyboardInterrupt:
                    print("\n👋 Thanks for using Reddit Project Idea Finder Agent!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        # Run the interactive loop
        asyncio.run(interactive_loop())


def main():
    """Main function to demonstrate the Reddit Project Idea Finder Agent."""
    print("🚀 Initializing Reddit Project Idea Finder Agent...")
    
    # Create the agent
    agent = RedditProjectIdeaFinderAgent()
    
    # Check if running interactively or with command line arguments
    import sys
    
    if len(sys.argv) > 1:
        # Command line query
        query = " ".join(sys.argv[1:])
        print(f"Running with query: {query}")
        
        async def run_query():
            await agent.find_project_ideas(query)
        
        asyncio.run(run_query())
    else:
        # Interactive mode
        agent.run_interactive_session()


if __name__ == "__main__":
    main()