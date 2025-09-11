# Reddit Project Idea Finder Agent

This project is an intelligent business opportunity discovery agent that analyzes Reddit discussions to identify profitable project opportunities. The agent uses Google's Agent Development Kit (ADK) to orchestrate sophisticated analysis of Reddit content, finding user pain points, unmet needs, and market gaps. It combines Reddit insights with competitive market research through Google Search integration to provide evidence-based business recommendations.

The target audience includes entrepreneurs, developers, startup founders, and anyone looking to discover validated business opportunities based on real user problems discussed in Reddit communities.

## Tech Stack

### Backend & Core
- **Python 3.8+**: Primary language for all components
- **Google ADK (Agent Development Kit)**: Multi-agent orchestration and planning
- **PRAW (Python Reddit API Wrapper)**: Reddit API integration for discussion analysis
- **Google Search API**: Built-in tool for competitive analysis and market research
- **Gemini 2.0 Flash**: Language model for reasoning and analysis

### Agent Architecture
- **Multi-Agent System**: Specialized sub-agents for different tasks
  - `reddit_analyzer`: Custom tools for Reddit analysis and business evaluation
  - `market_researcher`: Google Search integration for competitive analysis
- **Planning Systems**: PlanReActPlanner and BuiltInPlanner for systematic reasoning
- **Tool Orchestration**: Custom tools combined with built-in Google tools

### Development & Environment
- **Virtual Environment**: Python venv for dependency isolation
- **Environment Variables**: `.env` file for API credentials (Reddit, optional Google)
- **Jupyter Notebooks**: Interactive development and testing in `dev/` folder

## Project Structure

```
reddit-idea-finder/
├── src/                                    # Source code directory
│   ├── reddit_idea_finder.py             # Core Reddit API functionality
│   ├── reddit_project_idea_finder_agent.py        # Main enhanced agent (v2)
│   ├── reddit_project_idea_finder_agent_enhanced.py # Enhanced agent with merged capabilities
│   ├── reddit_scraper_scraperapi.py      # Alternative scraping implementation
│   └── test_reddit_search.ipynb          # Basic testing notebook
├── dev/                                   # Development and planning
│   ├── planner.txt                        # Development planning document
│   ├── reddit_finder.ipynb               # Core development notebook
│   └── test_google_adk_playground.ipynb  # Advanced testing and development
├── demo_agent.py                          # Basic demo script
├── demo_enhanced_agent.py                 # Enhanced demo with competitive analysis
├── test_enhanced_merge.py                 # Capability verification script
├── requirements.txt                       # Python dependencies
├── .env.template                          # Environment variable template
├── README.md                              # Project documentation
└── .github/
    └── copilot-instructions.md           # This file
```

## Coding Standards and Guidelines

### Python Code Style
- Always use type hints for function parameters and return values
- Use descriptive variable and function names
- Follow PEP 8 formatting standards
- Use docstrings for all classes and functions
- Import organization: standard library, third-party, local imports

### Agent Development Patterns
- **Multi-Agent Architecture**: Separate concerns between Reddit analysis and market research
- **Tool Separation**: Custom tools and built-in tools must be in separate agents (ADK constraint)
- **Async/Await**: Use async patterns for agent execution and tool coordination
- **Error Handling**: Comprehensive exception handling with user-friendly error messages

### Security and API Usage
- Store all credentials in `.env` file, never in code
- Use read-only Reddit API access
- Respect API rate limits and terms of service
- Validate all user inputs before processing

### Testing and Validation
- Unit tests for core Reddit functionality
- Integration tests for agent workflows
- Manual testing through demo scripts and notebooks
- Capability verification through test scripts

## Environment Setup and Build Instructions

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials (free from reddit.com/prefs/apps)
- Optional: Google API key for enhanced performance

### Initial Setup
```bash
# 1. Clone the repository and navigate to directory
cd reddit-idea-finder

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.template .env
# Edit .env with your Reddit API credentials:
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_SECRET=your_client_secret
# REDDIT_USER_AGENT=your_app_name
```

### Running the Application

**Basic Demo:**
```bash
python demo_agent.py
```

**Enhanced Demo with Competitive Analysis:**
```bash
python demo_enhanced_agent.py
```

**Interactive Agent:**
```bash
python src/reddit_project_idea_finder_agent_enhanced.py
```

**Command Line Usage:**
```bash
python src/reddit_project_idea_finder_agent_enhanced.py "Find 3 profitable SaaS ideas for developers"
```

### Development and Testing

**Interactive Development:**
```bash
jupyter notebook dev/test_google_adk_playground.ipynb
```

**Verify Capabilities:**
```bash
python test_enhanced_merge.py
```

**Test Core Functionality:**
```bash
cd src && python -c "from reddit_idea_finder import RedditIdeaFinder; print('Core Reddit functionality working')"
```

## Key Files and Components

### Core Agent Files
- `src/reddit_project_idea_finder_agent_enhanced.py`: **Primary agent file** with all enhanced capabilities
- `src/reddit_idea_finder.py`: Core Reddit API wrapper and search functionality
- `src/reddit_project_idea_finder_agent.py`: Alternative agent implementation

### Tools and Capabilities
- `search_reddit_for_ideas()`: Searches Reddit discussions for pain points and opportunities
- `evaluate_business_opportunity()`: Multi-criteria business evaluation with scoring
- `analyze_market_competition()`: Competitive analysis via Google Search integration

### Development Resources
- `dev/test_google_adk_playground.ipynb`: Main development notebook with examples
- `demo_enhanced_agent.py`: Working example of enhanced agent capabilities
- `test_enhanced_merge.py`: Verification script for all features

## Configuration Files
- `.env`: API credentials and configuration (create from `.env.template`)
- `requirements.txt`: Python dependencies including Google ADK, PRAW, python-dotenv
- `.github/copilot-instructions.md`: This instructions file

## Available Scripts and Resources

### Demo Scripts
- `demo_agent.py`: Basic agent demonstration
- `demo_enhanced_agent.py`: Enhanced agent with Google Search integration
- `test_enhanced_merge.py`: Capability verification and testing

### Development Notebooks
- `dev/test_google_adk_playground.ipynb`: Interactive development environment
- `src/test_reddit_search.ipynb`: Basic Reddit functionality testing

### Validation Commands
```bash
# Test imports
python -c "from src.reddit_project_idea_finder_agent_enhanced import RedditProjectIdeaFinderAgent; print('✅ Agent imports successfully')"

# Test Reddit connection
python -c "from src.reddit_idea_finder import RedditIdeaFinder; r = RedditIdeaFinder(); print('✅ Reddit API connection working')"

# Run capability test
python test_enhanced_merge.py
```

## Common Issues and Solutions

### Reddit API Issues
- **Error**: "Reddit API connection failed" → Check `.env` file has correct credentials
- **Error**: "PRAW async warnings" → Expected behavior, agent functions normally
- **Rate limiting** → Reduce search frequency, respect Reddit's API limits

### Agent Execution Issues
- **Tool mixing errors** → Use multi-agent architecture (reddit_analyzer + market_researcher)
- **Model compatibility** → Ensure using gemini-2.0-flash for Google Search features
- **Import errors** → Activate virtual environment and install requirements

### Environment Issues
- **Missing dependencies** → Run `pip install -r requirements.txt`
- **Path issues** → Run commands from project root directory
- **Credential issues** → Verify `.env` file exists and has correct format

## Project Guidelines for Contributors

### When Adding New Features
- Follow the multi-agent pattern for tool separation
- Add comprehensive error handling and user feedback
- Update both demo scripts and notebooks with examples
- Test new features with the verification script

### When Modifying Agent Behavior
- Preserve backward compatibility with existing demos
- Update agent instructions and prompts appropriately
- Test with various query types and edge cases
- Document any new dependencies or setup requirements

### When Working with APIs
- Always use environment variables for credentials
- Implement proper rate limiting and error handling
- Follow each API's terms of service and best practices
- Add fallback behavior for API failures

## Trust These Instructions

These instructions are comprehensive and up-to-date as of the project's current state. When working on this project:

- **Trust the multi-agent architecture** - it's required due to ADK tool constraints
- **Use the enhanced agent file** - `reddit_project_idea_finder_agent_enhanced.py` has all capabilities
- **Follow the setup steps exactly** - they've been tested and validated
- **Use the demo scripts** - they demonstrate working functionality

Only search for additional information if these instructions are incomplete or you encounter errors not covered in the "Common Issues" section.
