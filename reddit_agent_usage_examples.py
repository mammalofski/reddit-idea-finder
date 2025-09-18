#!/usr/bin/env python3
"""
Reddit Project Idea Finder Agent - Comprehensive Usage Examples

This file demonstrates all capabilities of the Reddit Project Idea Finder Agent,
including different usage patterns, planner types, and business domains.

Author: GitHub Copilot
Created: 2025-09-17
"""

import sys
import os
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing agent: {e}")
    print("Make sure you're running this from the project root and have all dependencies installed.")
    AGENT_AVAILABLE = False

class RedditAgentUsageExamples:
    """
    Comprehensive examples for using the Reddit Project Idea Finder Agent.
    
    Demonstrates all agent capabilities including:
    - Different planner types and their use cases
    - Various business domain queries
    - Batch processing and automation
    - Error handling and best practices
    """
    
    def __init__(self):
        """Initialize the usage examples class."""
        self.agents = {}
        self.results_log = []
        
    # =================================================================
    # BASIC USAGE EXAMPLES
    # =================================================================
    
    async def basic_usage_example(self):
        """Demonstrate basic agent usage with default settings."""
        print("\n" + "="*80)
        print("🚀 BASIC USAGE EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        # Create agent with default settings (plan_react planner)
        agent = RedditProjectIdeaFinderAgent()
        
        # Simple query
        query = "Find 3 profitable SaaS ideas for small businesses"
        print(f"Query: {query}")
        
        try:
            result = await agent.find_project_ideas(query)
            self._log_result("basic_usage", query, result)
            return result
        except Exception as e:
            print(f"❌ Error in basic usage: {e}")
            return None
    
    async def interactive_mode_demo(self):
        """Demonstrate interactive mode usage."""
        print("\n" + "="*80)
        print("🎮 INTERACTIVE MODE DEMO")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        print("""
Interactive Mode allows you to have a conversation with the agent.
To run interactive mode, use:

```python
agent = RedditProjectIdeaFinderAgent()
agent.run_interactive_session()
```

Or from command line:
```bash
python src/reddit_project_idea_finder_agent_enhanced.py
```

Example queries for interactive mode:
- "Find AI startup ideas from Reddit discussions"
- "What are developers complaining about in productivity tools?"
- "Discover e-commerce pain points that could become profitable businesses"
- "Find micro SaaS opportunities in the remote work space"
""")
    
    # =================================================================
    # PLANNER COMPARISON EXAMPLES
    # =================================================================
    
    async def compare_planners_example(self):
        """Compare different planner types on the same query."""
        print("\n" + "="*80)
        print("🧠 PLANNER COMPARISON EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        query = "Find developer productivity pain points that could become micro SaaS products"
        planners = ["plan_react", "built_in", "none"]
        results = {}
        
        for planner_type in planners:
            print(f"\n--- Testing {planner_type.upper()} Planner ---")
            
            try:
                agent = RedditProjectIdeaFinderAgent(planner_type=planner_type)
                start_time = datetime.now()
                
                result = await agent.find_project_ideas(query)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                results[planner_type] = {
                    "result": result,
                    "duration": duration,
                    "timestamp": end_time.isoformat()
                }
                
                print(f"✅ {planner_type} completed in {duration:.2f} seconds")
                
            except Exception as e:
                print(f"❌ Error with {planner_type}: {e}")
                results[planner_type] = {"error": str(e)}
        
        # Summary comparison
        print("\n--- PLANNER COMPARISON SUMMARY ---")
        for planner, data in results.items():
            if "error" not in data:
                print(f"{planner.upper()}: {data['duration']:.2f}s")
            else:
                print(f"{planner.upper()}: ERROR - {data['error']}")
        
        self._log_result("planner_comparison", query, results)
        return results
    
    # =================================================================
    # BUSINESS DOMAIN EXAMPLES
    # =================================================================
    
    async def ai_startup_ideas_example(self):
        """Find AI/ML startup opportunities."""
        print("\n" + "="*80)
        print("🤖 AI STARTUP IDEAS EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
        
        queries = [
            "Find AI startup ideas from machine learning community pain points",
            "What are developers saying about AI tools that don't work well?",
            "Discover gaps in current AI/ML development workflows"
        ]
        
        results = {}
        for i, query in enumerate(queries, 1):
            print(f"\n--- AI Query {i}: {query[:50]}... ---")
            
            try:
                result = await agent.find_project_ideas(query)
                results[f"ai_query_{i}"] = {"query": query, "result": result}
                print(f"✅ AI Query {i} completed")
            except Exception as e:
                print(f"❌ Error in AI Query {i}: {e}")
                results[f"ai_query_{i}"] = {"query": query, "error": str(e)}
        
        self._log_result("ai_startup_ideas", "Multiple AI queries", results)
        return results
    
    async def saas_opportunities_example(self):
        """Find SaaS business opportunities."""
        print("\n" + "="*80)
        print("💼 SAAS OPPORTUNITIES EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
        
        queries = [
            "Find micro SaaS ideas for small businesses under $50/month",
            "What SaaS tools do entrepreneurs say they need but can't find?",
            "Discover B2B SaaS gaps in project management and productivity"
        ]
        
        results = {}
        for i, query in enumerate(queries, 1):
            print(f"\n--- SaaS Query {i}: {query[:50]}... ---")
            
            try:
                result = await agent.find_project_ideas(query)
                results[f"saas_query_{i}"] = {"query": query, "result": result}
                print(f"✅ SaaS Query {i} completed")
            except Exception as e:
                print(f"❌ Error in SaaS Query {i}: {e}")
                results[f"saas_query_{i}"] = {"query": query, "error": str(e)}
        
        self._log_result("saas_opportunities", "Multiple SaaS queries", results)
        return results
    
    async def ecommerce_ideas_example(self):
        """Find e-commerce business opportunities."""
        print("\n" + "="*80)
        print("🛒 E-COMMERCE IDEAS EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="built_in")  # Different planner
        
        query = "Find e-commerce pain points and dropshipping opportunities from Reddit discussions"
        
        try:
            result = await agent.find_project_ideas(query)
            self._log_result("ecommerce_ideas", query, result)
            return result
        except Exception as e:
            print(f"❌ Error in e-commerce example: {e}")
            return None
    
    # =================================================================
    # ADVANCED USAGE EXAMPLES
    # =================================================================
    
    async def batch_processing_example(self):
        """Demonstrate batch processing of multiple queries."""
        print("\n" + "="*80)
        print("📦 BATCH PROCESSING EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        # Create one agent instance for efficiency
        agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
        
        # Batch of queries across different domains
        batch_queries = [
            ("Developer Tools", "Find developer productivity pain points for CLI tools"),
            ("Remote Work", "Discover remote work challenges that could become products"),
            ("Content Creation", "What do content creators complain about most?"),
            ("Small Business", "Find small business automation opportunities under $100/month"),
            ("Student Market", "Discover student productivity and study pain points")
        ]
        
        results = {}
        total_start = datetime.now()
        
        for category, query in batch_queries:
            print(f"\n--- Processing: {category} ---")
            query_start = datetime.now()
            
            try:
                result = await agent.find_project_ideas(query)
                query_end = datetime.now()
                duration = (query_end - query_start).total_seconds()
                
                results[category.lower().replace(" ", "_")] = {
                    "category": category,
                    "query": query,
                    "result": result,
                    "duration": duration
                }
                
                print(f"✅ {category} completed in {duration:.2f}s")
                
            except Exception as e:
                print(f"❌ Error processing {category}: {e}")
                results[category.lower().replace(" ", "_")] = {
                    "category": category,
                    "query": query,
                    "error": str(e)
                }
        
        total_end = datetime.now()
        total_duration = (total_end - total_start).total_seconds()
        
        print(f"\n--- BATCH PROCESSING SUMMARY ---")
        print(f"Total time: {total_duration:.2f} seconds")
        print(f"Queries processed: {len(batch_queries)}")
        print(f"Average time per query: {total_duration/len(batch_queries):.2f}s")
        
        self._log_result("batch_processing", "Multiple domain queries", results)
        return results
    
    async def competitive_analysis_focus_example(self):
        """Demonstrate competitive analysis capabilities."""
        print("\n" + "="*80)
        print("🔍 COMPETITIVE ANALYSIS FOCUS EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
        
        # Query specifically asking for competitive analysis
        query = """
        Find a profitable project management tool opportunity by:
        1. Analyzing Reddit discussions about PM tool pain points
        2. Research existing competitors and their weaknesses
        3. Identify market gaps and differentiation opportunities
        4. Provide specific competitive positioning recommendations
        """
        
        try:
            result = await agent.find_project_ideas(query)
            self._log_result("competitive_analysis", query, result)
            return result
        except Exception as e:
            print(f"❌ Error in competitive analysis: {e}")
            return None
    
    # =================================================================
    # SPECIALIZED USAGE PATTERNS
    # =================================================================
    
    async def niche_market_discovery_example(self):
        """Find opportunities in niche markets."""
        print("\n" + "="*80)
        print("🎯 NICHE MARKET DISCOVERY EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
        
        niche_queries = [
            "Find profitable opportunities in the pet care automation space",
            "Discover underserved markets in accessibility technology",
            "What business opportunities exist in sustainable living products?"
        ]
        
        results = {}
        for i, query in enumerate(niche_queries, 1):
            print(f"\n--- Niche Market {i}: {query[:40]}... ---")
            
            try:
                result = await agent.find_project_ideas(query)
                results[f"niche_{i}"] = {"query": query, "result": result}
                print(f"✅ Niche Market {i} analysis completed")
            except Exception as e:
                print(f"❌ Error in Niche Market {i}: {e}")
                results[f"niche_{i}"] = {"query": query, "error": str(e)}
        
        self._log_result("niche_market_discovery", "Multiple niche queries", results)
        return results
    
    async def problem_validation_example(self):
        """Validate specific business problems."""
        print("\n" + "="*80)
        print("✅ PROBLEM VALIDATION EXAMPLE")
        print("="*80)
        
        if not AGENT_AVAILABLE:
            print("❌ Agent not available. Please check setup.")
            return
        
        agent = RedditProjectIdeaFinderAgent(planner_type="built_in")
        
        # Validate a specific problem hypothesis
        query = """
        I have an idea for a tool that helps freelancers track time and generate invoices automatically.
        Validate this problem by:
        1. Finding Reddit discussions about freelancer pain points
        2. Checking if time tracking and invoicing are real problems
        3. Researching existing solutions and their weaknesses
        4. Evaluating market size and willingness to pay
        """
        
        try:
            result = await agent.find_project_ideas(query)
            self._log_result("problem_validation", query, result)
            return result
        except Exception as e:
            print(f"❌ Error in problem validation: {e}")
            return None
    
    # =================================================================
    # UTILITY AND HELPER METHODS
    # =================================================================
    
    def _log_result(self, example_type: str, query: str, result: Any):
        """Log results for later analysis."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "example_type": example_type,
            "query": query,
            "result_type": type(result).__name__,
            "has_error": "error" in str(result).lower() if isinstance(result, str) else False
        }
        self.results_log.append(log_entry)
    
    def save_results_log(self, filename: str = "reddit_agent_results.json"):
        """Save results log to file."""
        log_file = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(log_file, 'w') as f:
                json.dump(self.results_log, f, indent=2)
            print(f"✅ Results log saved to {log_file}")
        except Exception as e:
            print(f"❌ Error saving results log: {e}")
    
    def print_usage_summary(self):
        """Print a summary of all available usage patterns."""
        print("\n" + "="*80)
        print("📋 REDDIT AGENT USAGE SUMMARY")
        print("="*80)
        
        usage_patterns = {
            "Basic Usage": "Simple single queries with default settings",
            "Interactive Mode": "Conversational interface for exploration",
            "Planner Comparison": "Test different reasoning approaches",
            "Domain-Specific": "Specialized queries for AI, SaaS, e-commerce",
            "Batch Processing": "Multiple queries efficiently processed",
            "Competitive Analysis": "Market research and competitor evaluation",
            "Niche Discovery": "Find opportunities in specialized markets",
            "Problem Validation": "Validate specific business hypotheses"
        }
        
        print("\nAvailable Usage Patterns:")
        for pattern, description in usage_patterns.items():
            print(f"  🔹 {pattern}: {description}")
        
        print(f"\nCommand Line Usage:")
        print(f"  python reddit_agent_usage_examples.py --example basic")
        print(f"  python reddit_agent_usage_examples.py --example ai")
        print(f"  python reddit_agent_usage_examples.py --example batch")
        print(f"  python reddit_agent_usage_examples.py --example all")
        
        print(f"\nProgrammatic Usage:")
        print(f"  examples = RedditAgentUsageExamples()")
        print(f"  await examples.basic_usage_example()")
        print(f"  await examples.saas_opportunities_example()")
    
    # =================================================================
    # MAIN EXECUTION METHODS
    # =================================================================
    
    async def run_all_examples(self):
        """Run all usage examples in sequence."""
        print("\n" + "="*100)
        print("🎯 RUNNING ALL REDDIT AGENT USAGE EXAMPLES")
        print("="*100)
        
        examples = [
            ("Basic Usage", self.basic_usage_example),
            ("Interactive Demo", self.interactive_mode_demo),
            ("Planner Comparison", self.compare_planners_example),
            ("AI Startup Ideas", self.ai_startup_ideas_example),
            ("SaaS Opportunities", self.saas_opportunities_example),
            ("E-commerce Ideas", self.ecommerce_ideas_example),
            ("Batch Processing", self.batch_processing_example),
            ("Competitive Analysis", self.competitive_analysis_focus_example),
            ("Niche Market Discovery", self.niche_market_discovery_example),
            ("Problem Validation", self.problem_validation_example)
        ]
        
        results = {}
        start_time = datetime.now()
        
        for name, example_func in examples:
            print(f"\n🚀 Running: {name}")
            try:
                result = await example_func()
                results[name.lower().replace(" ", "_")] = result
                print(f"✅ {name} completed successfully")
            except Exception as e:
                print(f"❌ {name} failed: {e}")
                results[name.lower().replace(" ", "_")] = {"error": str(e)}
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        print(f"\n" + "="*100)
        print(f"🎉 ALL EXAMPLES COMPLETED")
        print(f"Total execution time: {total_duration:.2f} seconds")
        print(f"Examples run: {len(examples)}")
        print(f"Results logged: {len(self.results_log)}")
        print("="*100)
        
        # Save results
        self.save_results_log()
        
        return results
    
    async def run_single_example(self, example_name: str):
        """Run a single example by name."""
        example_map = {
            "basic": self.basic_usage_example,
            "interactive": self.interactive_mode_demo,
            "planners": self.compare_planners_example,
            "ai": self.ai_startup_ideas_example,
            "saas": self.saas_opportunities_example,
            "ecommerce": self.ecommerce_ideas_example,
            "batch": self.batch_processing_example,
            "competitive": self.competitive_analysis_focus_example,
            "niche": self.niche_market_discovery_example,
            "validation": self.problem_validation_example
        }
        
        if example_name.lower() in example_map:
            return await example_map[example_name.lower()]()
        else:
            print(f"❌ Unknown example: {example_name}")
            print(f"Available examples: {', '.join(example_map.keys())}")
            return None


# =================================================================
# COMMAND LINE INTERFACE
# =================================================================

def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Reddit Project Idea Finder Agent - Usage Examples")
    parser.add_argument(
        "--example", 
        choices=["basic", "interactive", "planners", "ai", "saas", "ecommerce", 
                "batch", "competitive", "niche", "validation", "all", "summary"],
        default="summary",
        help="Which example to run (default: summary)"
    )
    parser.add_argument(
        "--save-log", 
        action="store_true",
        help="Save results to JSON log file"
    )
    
    args = parser.parse_args()
    
    # Create examples instance
    examples = RedditAgentUsageExamples()
    
    if args.example == "summary":
        examples.print_usage_summary()
        return
    
    # Run the selected example(s)
    async def run_examples():
        if args.example == "all":
            await examples.run_all_examples()
        else:
            await examples.run_single_example(args.example)
        
        if args.save_log:
            examples.save_results_log()
    
    # Execute
    try:
        asyncio.run(run_examples())
    except KeyboardInterrupt:
        print("\n👋 Examples interrupted by user")
    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()


# =================================================================
# QUICK START EXAMPLES FOR COPY-PASTE
# =================================================================

"""
QUICK START EXAMPLES - Copy and paste these into your own code:

1. BASIC USAGE:
```python
import asyncio
from reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent

async def find_ideas():
    agent = RedditProjectIdeaFinderAgent()
    result = await agent.find_project_ideas("Find 3 profitable AI startup ideas")
    print(result)

asyncio.run(find_ideas())
```

2. WITH DIFFERENT PLANNER:
```python
agent = RedditProjectIdeaFinderAgent(planner_type="built_in")
result = await agent.find_project_ideas("Find SaaS opportunities for developers")
```

3. INTERACTIVE MODE:
```python
agent = RedditProjectIdeaFinderAgent()
agent.run_interactive_session()  # Starts interactive chat
```

4. COMMAND LINE:
```bash
# Interactive mode
python src/reddit_project_idea_finder_agent_enhanced.py

# Direct query
python src/reddit_project_idea_finder_agent_enhanced.py "Find micro SaaS ideas"

# With specific planner
python src/reddit_project_idea_finder_agent_enhanced.py --planner built_in "Find AI opportunities"
```

5. BATCH PROCESSING:
```python
queries = [
    "Find developer tool opportunities",
    "Discover e-commerce pain points",
    "What do remote workers complain about?"
]

agent = RedditProjectIdeaFinderAgent()
results = []
for query in queries:
    result = await agent.find_project_ideas(query)
    results.append(result)
```

6. COMPETITIVE ANALYSIS FOCUS:
```python
query = '''
Find a profitable project management tool opportunity by:
1. Analyzing Reddit discussions about PM tool pain points
2. Research existing competitors and their weaknesses  
3. Identify market gaps and differentiation opportunities
'''

agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
result = await agent.find_project_ideas(query)
```
"""