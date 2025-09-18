# Reddit Project Idea Finder Agent - Setup & Usage Guide

## Quick Setup

### 1. Prerequisites
```bash
# Python 3.8 or higher
python --version

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Reddit API Setup
1. Go to https://reddit.com/prefs/apps
2. Create a new application (script type)
3. Copy Client ID and Secret
4. Create `.env` file:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=YourAppName/1.0
```

### 4. Test Installation
```bash
python reddit_agent_usage_examples.py --example basic
```

## Usage Patterns

### Simple Usage
```python
import asyncio
from src.reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent

async def find_ideas():
    agent = RedditProjectIdeaFinderAgent()
    result = await agent.find_project_ideas("Find 3 profitable SaaS ideas")
    print(result)

asyncio.run(find_ideas())
```

### Interactive Mode
```bash
python src/reddit_project_idea_finder_agent_enhanced.py
```

### Command Line Queries
```bash
# Basic query
python src/reddit_project_idea_finder_agent_enhanced.py "Find AI startup opportunities"

# With specific planner
python src/reddit_project_idea_finder_agent_enhanced.py --planner built_in "Find developer tools pain points"
```

### All Examples
```bash
python reddit_agent_usage_examples.py --example all
```

## Agent Capabilities

### Core Features
- **Multi-Agent Architecture**: Specialized sub-agents for Reddit analysis and market research
- **Advanced Planning**: Three planner types (plan_react, built_in, none)
- **Reddit Analysis**: Deep analysis of discussions, comments, and pain points
- **Market Research**: Competitive analysis via Google Search integration
- **Business Evaluation**: Multi-criteria scoring and recommendations

### Available Tools
1. `search_reddit_for_ideas()`: Find pain points and opportunities
2. `evaluate_business_opportunity()`: Score and evaluate ideas
3. `analyze_market_competition()`: Research competitors and market gaps

### Planner Types
- **plan_react** (default): Structured reasoning with explicit planning
- **built_in**: Basic planning with thinking capabilities  
- **none**: Direct execution without planning

## Common Issues & Solutions

### Reddit API Issues
**Problem**: "Reddit API connection failed"
**Solution**: 
1. Check `.env` file exists and has correct credentials
2. Verify Reddit app is "script" type
3. Ensure REDDIT_USER_AGENT is descriptive

### Import Errors
**Problem**: "Cannot import RedditProjectIdeaFinderAgent"
**Solution**:
1. Run from project root directory
2. Check virtual environment is activated
3. Install dependencies: `pip install -r requirements.txt`

### Google ADK Issues
**Problem**: "google.adk module not found"
**Solution**:
```bash
pip install google-adk
# or
pip install --upgrade google-adk
```

### Performance Issues
**Problem**: Agent runs slowly
**Solutions**:
1. Use `planner_type="none"` for faster execution
2. Limit Reddit search results in queries
3. Use `built_in` planner instead of `plan_react`

## Example Queries

### Business Domains
- **AI/ML**: "Find AI startup ideas from machine learning community pain points"
- **SaaS**: "Discover micro SaaS opportunities under $50/month"
- **E-commerce**: "Find e-commerce automation opportunities for small businesses"
- **Developer Tools**: "What developer productivity pain points could become products?"

### Analysis Types
- **Market Research**: "Research competitors for project management tools and find gaps"
- **Problem Validation**: "Validate if freelancers really need better time tracking tools"
- **Niche Discovery**: "Find profitable opportunities in pet care automation"

## Running Examples

```bash
# See all available examples
python reddit_agent_usage_examples.py --example summary

# Run specific examples
python reddit_agent_usage_examples.py --example basic
python reddit_agent_usage_examples.py --example ai
python reddit_agent_usage_examples.py --example saas
python reddit_agent_usage_examples.py --example batch

# Run all examples and save results
python reddit_agent_usage_examples.py --example all --save-log
```

## Integration Examples

### In Your Own Project
```python
from src.reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent

class MyBusinessAnalyzer:
    def __init__(self):
        self.agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")
    
    async def analyze_market(self, domain):
        query = f"Find profitable opportunities in {domain}"
        return await self.agent.find_project_ideas(query)
```

### Batch Processing
```python
async def analyze_multiple_domains(domains):
    agent = RedditProjectIdeaFinderAgent()
    results = {}
    
    for domain in domains:
        query = f"Find {domain} business opportunities"
        results[domain] = await agent.find_project_ideas(query)
    
    return results
```

## File Structure

```
reddit-idea-finder/
├── src/
│   ├── reddit_project_idea_finder_agent_enhanced.py  # Main agent
│   └── reddit_idea_finder.py                         # Reddit API wrapper
├── reddit_agent_usage_examples.py                    # Usage examples
├── requirements.txt                                   # Dependencies
├── .env                                              # API credentials
└── README.md                                         # Documentation
```

## Support

For issues:
1. Check this setup guide first
2. Verify all dependencies are installed
3. Test with basic examples before advanced usage
4. Check Reddit API credentials and quota

The agent coordinates specialized sub-agents to provide comprehensive business opportunity analysis from Reddit discussions combined with competitive market research.