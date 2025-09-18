#!/usr/bin/env python3
"""
Reddit Project Idea Finder Agent - Intelligent business opportunity discovery using Google ADK

This agent analyzes Reddit discussions to identify profitable project opportunities
by finding user pain points, unmet needs, and market gaps. Enhanced with advanced
planning capabilities for more systematic and thorough analysis.

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
from google.adk.planners import PlanReActPlanner, BuiltInPlanner
from google.adk.tools import google_search, agent_tool
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
    Enhanced with planning capabilities for systematic opportunity discovery.
    """
    
    def __init__(self, model="gemini-2.5-flash", planner_type="plan_react"):
        """
        Initialize the Reddit Project Idea Finder Agent.
        
        Args:
            model (str): Model to use for the agent (default: gemini-2.5-flash)
            planner_type (str): Type of planner to use:
                - "plan_react": PlanReActPlanner for structured reasoning (default)
                - "built_in": BuiltInPlanner with thinking capabilities
                - "none": No planner (basic agent)
        """
        self.model = model
        self.planner_type = planner_type
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
        """Set up the agent's tools for Reddit analysis, opportunity evaluation, and competitive analysis."""
        
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
                    "insights": []
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
                
                return {
                    "status": "success",
                    "query": query,
                    "focus_area": focus_area,
                    "subreddits_searched": target_subreddits,
                    "total_posts_found": len(posts),
                    "quality_posts": len(quality_posts),
                    "posts": quality_posts[:5],  # Return top 5 for analysis
                    "insights": insights
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Search failed: {str(e)}",
                    "posts": [],
                    "insights": []
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
        
        def analyze_market_competition(
            idea_description: str,
            target_keywords: str,
            market_segment: str = "general"
        ) -> Dict[str, Any]:
            """
            Tool to analyze market competition and existing solutions using Google Search.
            
            Args:
                idea_description (str): Description of the business idea to research
                target_keywords (str): Keywords to search for existing solutions
                market_segment (str): Market segment to focus on (e.g., "saas", "mobile apps", "ai tools")
            
            Returns:
                dict: Competitive analysis with existing solutions, gaps, and differentiation opportunities
            """
            print(f"🔍 Analyzing market competition for: {idea_description[:50]}...")
            
            # This function will be enhanced by the agent's google_search tool
            # The agent will automatically use google_search when this tool is called
            analysis_prompt = f"""
            Research the competitive landscape for this business idea: {idea_description}
            
            Search for:
            1. Existing solutions using keywords: {target_keywords}
            2. Competitors in the {market_segment} market
            3. Pricing models and features offered
            4. User reviews and complaints about existing solutions
            5. Market gaps and unmet needs
            
            Provide insights on:
            - Top 3-5 existing competitors
            - Common features and pricing
            - User complaints and missing features
            - Market differentiation opportunities
            - Barriers to entry and competitive advantages
            """
            
            return {
                "status": "analysis_requested",
                "idea": idea_description,
                "search_keywords": target_keywords,
                "market_segment": market_segment,
                "analysis_prompt": analysis_prompt,
                "competitive_factors": {
                    "market_saturation": "To be analyzed via Google Search",
                    "existing_solutions": "To be identified via Google Search", 
                    "pricing_models": "To be researched via Google Search",
                    "user_complaints": "To be discovered via Google Search",
                    "differentiation_opportunities": "To be evaluated via Google Search"
                },
                "search_strategy": [
                    f"{target_keywords} competitors",
                    f"{target_keywords} tools alternatives",
                    f"{target_keywords} reviews complaints",
                    f"{market_segment} {target_keywords} pricing",
                    f"best {target_keywords} software 2024"
                ]
            }
        
        # Store tools as instance methods
        self.search_reddit_for_ideas = search_reddit_for_ideas
        self.evaluate_business_opportunity = evaluate_business_opportunity
        self.analyze_market_competition = analyze_market_competition
    
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
        """Create the main Reddit Project Idea Finder Agent with specialized sub-agents for different tasks."""
        
        # Create specialized sub-agents
        # 1. Reddit Analysis Agent (custom tools)
        reddit_agent = Agent(
            name="reddit_analyzer",
            model=self.model,
            description="Specialized agent for analyzing Reddit discussions and evaluating business opportunities",
            instruction="""You specialize in analyzing Reddit discussions to identify business opportunities.
            
Your capabilities:
- Search Reddit for user pain points and problems
- Extract insights from posts and comments
- Evaluate business opportunities based on evidence
- Assess market potential and implementation feasibility

Always provide detailed analysis with supporting evidence from Reddit discussions.""",
            tools=[self.search_reddit_for_ideas, self.evaluate_business_opportunity, self.analyze_market_competition]
        )
        
        # 2. Market Research Agent (Google Search)
        market_research_agent = Agent(
            name="market_researcher", 
            model=self.model,
            description="Specialized agent for competitive analysis and market research using Google Search",
            instruction="""You specialize in market research and competitive analysis.
            
Your capabilities:
- Research existing competitors and solutions
- Analyze market trends and demands
- Identify pricing models and features
- Discover market gaps and opportunities
- Validate business ideas through search

Use Google Search to provide comprehensive market intelligence and competitive insights.""",
            tools=[google_search]
        )
        
        # Configure planner based on type
        planner = None
        enhanced_instruction = """You are a sophisticated business opportunity analyst that coordinates specialized teams to discover profitable project ideas from Reddit discussions and validate them through market research.

Your systematic approach:
1. **Query Analysis**: Interpret user requests to understand what type of opportunities they're seeking
2. **Team Coordination**: Delegate tasks to specialized sub-agents:
   - reddit_analyzer: For analyzing Reddit discussions and evaluating opportunities
   - market_researcher: For competitive analysis and market validation
3. **Strategic Planning**: Develop a comprehensive analysis strategy with multiple angles
4. **Synthesis & Report**: Combine insights from both agents to provide comprehensive recommendations

Advanced Guidelines:
- PLAN before acting: Create a strategy for comprehensive opportunity discovery
- Use reddit_analyzer to find and evaluate opportunities from Reddit discussions
- Use market_researcher to validate opportunities and research competition
- Focus on real problems people are actively discussing
- Research competition thoroughly before recommending opportunities
- Provide specific, actionable recommendations with supporting evidence
- Synthesize insights from both Reddit analysis and market research

You coordinate a team of specialists to provide the most comprehensive business opportunity analysis possible."""

        if self.planner_type == "plan_react":
            planner = PlanReActPlanner()
            print("🧠 Using PlanReActPlanner for structured reasoning")
        elif self.planner_type == "built_in":
            planner = BuiltInPlanner()
            print("🧠 Using BuiltInPlanner for basic planning")
        else:
            print("🧠 Using basic agent without planner")
        
        # Create the main coordinating agent with sub-agents
        if planner:
            self.agent = Agent(
                name="reddit_project_idea_finder",
                model=self.model,
                planner=planner,
                description="An intelligent agent that coordinates specialized teams to discover profitable project opportunities by analyzing Reddit discussions and validating them through comprehensive market research.",
                instruction=enhanced_instruction,
                tools=[agent_tool.AgentTool(agent=reddit_agent), agent_tool.AgentTool(agent=market_research_agent)]
            )
        else:
            self.agent = Agent(
                name="reddit_project_idea_finder",
                model=self.model,
                description="An intelligent agent that coordinates specialized teams to discover profitable project opportunities by analyzing Reddit discussions and validating them through comprehensive market research.",
                instruction="""You are a sophisticated business opportunity analyst that coordinates specialized teams to discover profitable project ideas from Reddit discussions and validate them through market research.

Your process:
1. **Query Analysis**: Interpret user requests to understand what type of opportunities they're seeking
2. **Team Coordination**: Delegate tasks to specialized sub-agents:
   - reddit_analyzer: For analyzing Reddit discussions and evaluating opportunities  
   - market_researcher: For competitive analysis and market validation using Google Search
3. **Strategic Analysis**: Develop comprehensive understanding through both sources
4. **Synthesis & Report**: Combine insights to provide well-researched recommendations

Enhanced Capabilities:
- Coordinate Reddit analysis with competitive market research
- Validate opportunities through multiple information sources
- Identify market gaps and differentiation opportunities
- Provide evidence-based recommendations with competitive context

Guidelines:
- Use reddit_analyzer to find and evaluate opportunities from Reddit discussions
- Use market_researcher to validate opportunities and research existing solutions
- Focus on real problems people are actively discussing
- Research competition thoroughly before recommending opportunities
- Provide specific, actionable recommendations with supporting evidence from both sources
- Synthesize insights from Reddit analysis AND market research for comprehensive recommendations

You coordinate specialists to provide the most comprehensive business opportunity analysis possible.""",
                tools=[agent_tool.AgentTool(agent=reddit_agent), agent_tool.AgentTool(agent=market_research_agent)]
            )
        
        print(f"✅ Reddit Project Idea Finder Agent created: '{self.agent.name}'")
        print(f"Model: {self.agent.model}")
        print(f"Planner: {self.planner_type}")
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
        print(f"""
🤖 Reddit Project Idea Finder Agent - Interactive Mode (Planner: {self.planner_type})
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
    import argparse
    import sys
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Reddit Project Idea Finder Agent with Advanced Planning")
    parser.add_argument("query", nargs="*", help="Query for finding project ideas")
    parser.add_argument("--planner", choices=["plan_react", "built_in", "none"], 
                       default="plan_react", help="Type of planner to use (default: plan_react)")
    parser.add_argument("--model", default="gemini-2.0-flash", 
                       help="Model to use (default: gemini-2.0-flash)")
    
    args = parser.parse_args()
    
    print("🚀 Initializing Reddit Project Idea Finder Agent...")
    print(f"🧠 Planner: {args.planner}")
    print(f"🤖 Model: {args.model}")
    
    # Create the agent with specified configuration
    agent = RedditProjectIdeaFinderAgent(model=args.model, planner_type=args.planner)
    
    if args.query:
        # Command line query
        query = " ".join(args.query)
        print(f"Running with query: {query}")
        
        async def run_query():
            await agent.find_project_ideas(query)
        
        asyncio.run(run_query())
    else:
        # Interactive mode
        agent.run_interactive_session()


if __name__ == "__main__":
    main()
    
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
        """Create the main Reddit Project Idea Finder Agent with advanced planning capabilities."""
        
        # Configure planner based on type
        planner = None
        enhanced_instruction = """You are a sophisticated business opportunity analyst specializing in discovering profitable project ideas from Reddit discussions.

Your systematic approach:
1. **Query Analysis**: Interpret user requests to understand what type of opportunities they're seeking
2. **Strategic Planning**: Develop a comprehensive search strategy with multiple angles and follow-up investigations
3. **Systematic Search**: Use search_reddit_for_ideas to find relevant discussions about problems, pain points, and unmet needs
4. **Deep Analysis**: Examine posts and comments to identify patterns of user frustration and desired solutions
5. **Opportunity Evaluation**: Use evaluate_business_opportunity to assess market potential and feasibility
6. **Recursive Investigation**: If initial findings suggest promising areas, conduct follow-up searches for deeper insights
7. **Synthesis & Report**: Provide 3-5 well-researched project recommendations with clear reasoning

Advanced Guidelines:
- PLAN before acting: Create a strategy for comprehensive opportunity discovery
- Focus on real problems people are actively discussing
- Look for recurring complaints and feature requests across multiple subreddits
- Prioritize opportunities with strong evidence and market potential
- Consider implementation complexity and time-to-market
- Provide specific, actionable recommendations with supporting evidence
- Use recursive search to validate and deepen findings
- Synthesize insights from multiple sources for comprehensive analysis

Planning Instructions:
- When you receive a query, first PLAN your investigation strategy
- Identify key search terms, target subreddits, and investigation angles
- Plan follow-up searches based on initial findings
- Structure your analysis to cover market validation, competition, and implementation feasibility
"""

        if self.planner_type == "plan_react":
            planner = PlanReActPlanner()
            print("🧠 Using PlanReActPlanner for structured reasoning")
        elif self.planner_type == "built_in":
            # Configure thinking for Gemini models
            thinking_config = types.ThinkingConfig(
                include_thoughts=True,  # Include model's reasoning process
                thinking_budget=512     # Allow substantial thinking tokens
            )
            planner = BuiltInPlanner(thinking_config=thinking_config)
            print("🧠 Using BuiltInPlanner with thinking capabilities")
        else:
            print("🧠 Using basic agent without planner")
        
        # Create agent with or without planner
        if planner:
            self.agent = Agent(
                name="reddit_project_idea_finder",
                model=self.model,
                planner=planner,
                description="An intelligent agent that discovers profitable project opportunities by analyzing Reddit discussions. Uses advanced planning capabilities to systematically identify user pain points, unmet needs, and market gaps.",
                instruction=enhanced_instruction,
                tools=[self.search_reddit_for_ideas, self.evaluate_business_opportunity]
            )
        else:
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
5. **Recursive Investigation**: If initial findings suggest promising areas, conduct follow-up searches for deeper insights
6. **Report Generation**: Provide 3-5 well-researched project recommendations with clear reasoning

Guidelines:
- Focus on real problems people are actively discussing
- Look for recurring complaints and feature requests
- Prioritize opportunities with strong evidence and market potential
- Consider implementation complexity and time-to-market
- Provide specific, actionable recommendations
- Always include supporting evidence from Reddit discussions

You should be thorough but efficient, conducting multiple searches when needed to build a comprehensive understanding of opportunities.""",
                tools=[self.search_reddit_for_ideas, self.evaluate_business_opportunity]
            )
        
        print(f"✅ Reddit Project Idea Finder Agent created: '{self.agent.name}'")
        print(f"Model: {self.agent.model}")
        print(f"Planner: {self.planner_type}")
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
        print(f"""
🤖 Reddit Project Idea Finder Agent - Interactive Mode (Planner: {self.planner_type})
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
    import argparse
    import sys
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Reddit Project Idea Finder Agent with Advanced Planning")
    parser.add_argument("query", nargs="*", help="Query for finding project ideas")
    parser.add_argument("--planner", choices=["plan_react", "built_in", "none"], 
                       default="plan_react", help="Type of planner to use (default: plan_react)")
    parser.add_argument("--model", default="gemini-2.0-flash", 
                       help="Model to use (default: gemini-2.0-flash)")
    
    args = parser.parse_args()
    
    print("🚀 Initializing Reddit Project Idea Finder Agent...")
    print(f"🧠 Planner: {args.planner}")
    print(f"🤖 Model: {args.model}")
    
    # Create the agent with specified configuration
    agent = RedditProjectIdeaFinderAgent(model=args.model, planner_type=args.planner)
    
    if args.query:
        # Command line query
        query = " ".join(args.query)
        print(f"Running with query: {query}")
        
        async def run_query():
            await agent.find_project_ideas(query)
        
        asyncio.run(run_query())
    else:
        # Interactive mode
        agent.run_interactive_session()


if __name__ == "__main__":
    main()
