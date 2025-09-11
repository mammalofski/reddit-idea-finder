# Reddit Project Idea Finder Agent 🚀

An intelligent agent that discovers profitable project opportunities by analyzing Reddit discussions using Google's Agent Development Kit (ADK). The agent identifies user pain points, unmet needs, and market gaps, then validates them through comprehensive competitive analysis using Google Search.

## 🎯 Enhanced Features

- **Intelligent Reddit Analysis**: Searches across multiple subreddits to find real user problems and pain points
- **Google Search Integration**: Validates opportunities through competitive market research
- **Multi-Agent Architecture**: Coordinates specialized sub-agents for different analysis tasks
- **Advanced Planning**: Uses ADK planners for systematic and thorough opportunity discovery
- **Competitive Analysis**: Researches existing solutions, pricing models, and market gaps
- **Multi-Criteria Evaluation**: Assesses opportunities based on market potential, implementation complexity, and evidence strength
- **Recursive Search**: Conducts follow-up searches for deeper insights into promising opportunities
- **Evidence-Based Reasoning**: Links all recommendations to supporting Reddit posts and market research
- **Interactive CLI**: User-friendly command-line interface for discovering opportunities
- **Comprehensive Reporting**: Generates detailed project recommendations with scoring, competitive analysis, and next steps

## 🏗️ Architecture

The agent uses a sophisticated multi-agent architecture:

### Main Coordinator Agent
- Orchestrates the entire analysis process
- Delegates tasks to specialized sub-agents
- Synthesizes insights from multiple sources

### Specialized Sub-Agents
1. **Reddit Analyzer**: 
   - Discovers Reddit discussions about problems and opportunities
   - Evaluates business potential using multiple criteria
   - Extracts specific user frustrations and feature requests

2. **Market Researcher**: 
   - Conducts competitive analysis using Google Search
   - Validates market demand and identifies existing solutions
   - Analyzes pricing models and feature gaps

## 📋 Requirements

- Python 3.8+
- Reddit API credentials (free)
- Google API key (optional, for enhanced performance)

## 🚀 Quick Start

### 1. Installation

```bash
git clone <repository-url>
cd reddit-idea-finder
pip install -r requirements.txt
```

### 2. Setup Reddit API Credentials

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new app (select "script" type)
3. Copy the `.env.template` to `.env`
4. Add your credentials:

```bash
cp .env.template .env
# Edit .env with your Reddit credentials
```

### 3. Run the Enhanced Agent

**Interactive Mode:**
```bash
python src/reddit_project_idea_finder_agent.py
```

**Command Line Query:**
```bash
python src/reddit_project_idea_finder_agent.py "Find profitable AI startup ideas with competitive analysis"
```

**Enhanced Demo:**
```bash
python demo_enhanced_agent.py
```

## 💡 Example Queries

- "Find 3 profitable micro SaaS ideas for developers and research their competitive landscape"
- "What are some underserved markets in e-commerce with existing competition analysis?"
- "Discover AI startup opportunities in healthcare and validate market demand"
- "Find content creator tools that people would pay for and analyze existing solutions"

## 📊 Sample Enhanced Output

```
🎯 User Query: Find 2 profitable SaaS ideas for developers and research their competitive landscape

🔍 Analyzing Reddit discussions for developer pain points...
� Researching competitive landscape via Google Search...

📊 Agent Analysis Complete
================================================================================

**Open-Source Whiteboard/Infinite Canvas Tool:**
- Competition: Excalidraw, tldraw, OpenBoard, WBO, draw.io
- Key Features: Real-time collaboration, drawing tools, screen sharing
- Market Gap: Specialized tools for technical diagrams and architecture planning
- Recommendation: Focus on developer-specific use cases and integrations

**Open Source Alternative to Closed-Source Dev Tools:**
- Market Overview: Growing rapidly (16.7% CAGR), driven by cost savings
- Key Trends: Cloud-native development, AI-powered tools, DevSecOps
- Competitive Landscape: VS Code, GitLab, Jenkins, Docker ecosystem
- Recommendation: Target specific pain points in current toolchain gaps

Recommendations:
1. Focus on Differentiation: Identify clear unique value propositions
2. Targeted Market Research: Validate specific use cases with developers
3. Community Engagement: Build with developer community feedback
4. Sustainable Business Model: Consider open-source monetization strategies
================================================================================
```

## 🔧 Advanced Usage

### Planner Configuration

Choose different planning strategies:

```python
# Advanced planning with systematic reasoning
agent = RedditProjectIdeaFinderAgent(planner_type="plan_react")

# Basic planning
agent = RedditProjectIdeaFinderAgent(planner_type="built_in") 

# No planner (direct execution)
agent = RedditProjectIdeaFinderAgent(planner_type="none")
```

### Custom Focus Areas

The agent can target specific markets:

```python
# Available focus areas: ai, saas, ecommerce, developer, general
await agent.find_project_ideas("Find developer tools opportunities")
```

### Multi-Agent Coordination

The system automatically coordinates:
- **Reddit Analysis**: Pain point discovery and opportunity evaluation
- **Market Research**: Competitive analysis and validation via Google Search
- **Synthesis**: Combined insights for comprehensive recommendations

## 🎓 How It Works

1. **Query Processing**: Interprets user requests to understand opportunity types
2. **Strategic Planning**: Develops comprehensive analysis strategy (with planner)
3. **Parallel Analysis**: 
   - Reddit Analyzer searches discussions and evaluates opportunities
   - Market Researcher validates demand and analyzes competition via Google Search
4. **Insight Synthesis**: Combines Reddit insights with market research
5. **Report Generation**: Compiles actionable recommendations with evidence

## 📁 Project Structure

```
reddit-idea-finder/
├── src/
│   ├── reddit_idea_finder.py              # Core Reddit search functionality
│   └── reddit_project_idea_finder_agent.py # Enhanced ADK agent with Google Search
├── dev/
│   ├── test_google_adk_playground.ipynb    # Development and testing notebook
│   └── planner.txt                         # Development planning document
├── demo_agent.py                           # Basic demo script
├── demo_enhanced_agent.py                  # Enhanced demo with competitive analysis
├── requirements.txt                        # Python dependencies
├── .env.template                          # Environment variable template
└── README.md                              # This file
```

## 🧪 Testing

Run comprehensive tests:

```bash
# Test basic functionality
python demo_agent.py

# Test enhanced features with competitive analysis
python demo_enhanced_agent.py

# Interactive development and testing
jupyter notebook dev/test_google_adk_playground.ipynb
```

## 🛠️ Technical Details

### Enhanced Architecture
- **Google ADK**: Multi-agent orchestration with advanced planning
- **Sub-Agent Pattern**: Specialized agents for different analysis tasks
- **Google Search Integration**: Built-in tool for competitive research
- **PRAW**: Reddit API integration with comment analysis
- **Gemini 2.0 Flash**: Advanced language model for reasoning

### Key Enhancements
- `RedditAnalyzer`: Specialized Reddit analysis sub-agent
- `MarketResearcher`: Google Search-powered competitive analysis sub-agent
- `analyze_market_competition()`: Tool for competitive landscape research
- Advanced planning with `PlanReActPlanner` and `BuiltInPlanner`
- Multi-source evidence synthesis

## 🆕 What's New in v2.0

✅ **Google Search Integration**: Validate opportunities through market research
✅ **Multi-Agent Architecture**: Specialized sub-agents for different tasks  
✅ **Advanced Planning**: Systematic reasoning with ADK planners
✅ **Competitive Analysis**: Research existing solutions and market gaps
✅ **Enhanced Synthesis**: Combine Reddit insights with market validation
✅ **Improved Accuracy**: Evidence from multiple authoritative sources

## 🔐 Privacy & Ethics

- Uses Reddit's public API with read-only access
- Uses Google Search for publicly available market information
- Respects all API terms of service and rate limits
- Does not store personal user information
- Focuses on publicly available discussions and market trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google ADK team for the excellent agent development framework and built-in tools
- Reddit community for providing valuable discussions and insights
- PRAW developers for the robust Reddit API wrapper
- Google Search for enabling comprehensive market research

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-username/reddit-idea-finder/issues) page
2. Ensure your Reddit API credentials are correctly configured
3. Verify all dependencies are installed: `pip install -r requirements.txt`
4. Check Google API access for enhanced search features

---

**Happy opportunity hunting with enhanced market intelligence! 🎯🔍**
