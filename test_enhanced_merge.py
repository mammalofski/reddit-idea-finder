#!/usr/bin/env python3
"""
Test script to verify the enhanced agent has all capabilities merged successfully.
"""

import sys
import os
sys.path.append('src')

from reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent

def test_enhanced_capabilities():
    """Test that all enhanced capabilities are present."""
    print("🧪 Testing Enhanced Agent Capabilities")
    print("="*50)
    
    # Create agent instance
    agent = RedditProjectIdeaFinderAgent(model="gemini-2.0-flash", planner_type="plan_react")
    
    # Test 1: Check tools are available
    print("✅ Agent created successfully")
    print(f"📊 Agent name: {agent.agent.name}")
    print(f"🤖 Model: {agent.agent.model}")
    print(f"🧠 Planner type: {agent.planner_type}")
    print(f"🔧 Number of tools: {len(agent.agent.tools)}")
    
    # Test 2: Check tool functions exist
    required_tools = [
        'search_reddit_for_ideas',
        'evaluate_business_opportunity', 
        'analyze_market_competition'
    ]
    
    print("\n🔍 Checking Tool Availability:")
    for tool_name in required_tools:
        if hasattr(agent, tool_name):
            print(f"  ✅ {tool_name}")
        else:
            print(f"  ❌ {tool_name} - MISSING")
    
    # Test 3: Check multi-agent architecture
    print("\n🏗️ Multi-Agent Architecture:")
    if len(agent.agent.tools) >= 2:
        print("  ✅ Multiple agents/tools detected")
        for i, tool in enumerate(agent.agent.tools):
            print(f"    Tool {i+1}: {type(tool).__name__}")
    else:
        print("  ⚠️ Single agent detected")
    
    # Test 4: Check Google Search capability
    print("\n🔍 Google Search Integration:")
    try:
        from google.adk.tools import google_search
        print("  ✅ Google Search tool imported successfully")
    except ImportError:
        print("  ❌ Google Search tool not available")
    
    print("\n🎉 Enhanced Agent Test Complete!")
    print("="*50)

if __name__ == "__main__":
    test_enhanced_capabilities()
