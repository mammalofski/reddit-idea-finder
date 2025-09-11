# Reddit Project Idea Finder Agent 🚀

An intelligent agent that discovers profitable project opportunities by analyzing Reddit discussions using Google's Agent Development Kit (ADK). The agent identifies user pain points, unmet needs, and market gaps to suggest viable project ideas with evidence-based reasoning.

## 🎯 Features

- **Intelligent Reddit Analysis**: Searches across multiple subreddits to find real user problems and pain points
- **Multi-Criteria Evaluation**: Assesses opportunities based on market potential, implementation complexity, and evidence strength
- **Recursive Search**: Conducts follow-up searches for deeper insights into promising opportunities
- **Evidence-Based Reasoning**: Links all recommendations to supporting Reddit posts and comments
- **Interactive CLI**: User-friendly command-line interface for discovering opportunities
- **Comprehensive Reporting**: Generates detailed project recommendations with scoring, monetization strategies, and next steps

## 🏗️ Architecture

The agent uses Google ADK to orchestrate sophisticated analysis through specialized tools:

- **Search Tool**: Discovers Reddit discussions about problems and opportunities
- **Evaluation Tool**: Scores business potential using multiple criteria
- **Pain Point Extraction**: Identifies specific user frustrations and feature requests
- **Opportunity Assessment**: Evaluates market size, feasibility, and competition risk

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

### 3. Run the Agent

**Interactive Mode:**
```bash
python src/reddit_project_idea_finder_agent.py
```

**Command Line Query:**
```bash
python src/reddit_project_idea_finder_agent.py "Find profitable AI startup ideas"
```

## 💡 Example Queries

- "Find 3 profitable micro SaaS ideas based on developer pain points"
- "What are some underserved markets in e-commerce?"
- "Discover AI startup opportunities in healthcare"
- "Find content creator tools that people would pay for"

## 📊 Sample Output

```
🎯 User Query: Find profitable SaaS opportunities for content creators

🔍 Searching Reddit for ideas: 'content creator pain points saas' in focus area: 'saas'
📊 Evaluating opportunity: Content creators struggle to understand audience sentiment...

📊 Agent Analysis Complete
================================================================================

Here are 4 profitable SaaS opportunities for content creators:

1. **AI-Powered Content Insights Platform** (Score: 8.5/10)
   - Problem: Content creators struggle to understand audience sentiment
   - Target Market: Content creators, influencers
   - Monetization: SaaS subscription, usage-based pricing
   - Evidence: Multiple Reddit discussions about analytics frustrations

2. **Problem Validation Platform** (Score: 7.2/10)  
   - Problem: Entrepreneurs need better ways to validate ideas before building
   - Target Market: Startups, content creators
   - Monetization: Freemium model, per-validation pricing
   - Evidence: Recurring discussions about failed products

[... additional opportunities ...]
================================================================================
```

## 🔧 Advanced Usage

### Custom Focus Areas

The agent can search specific markets:

```python
# Available focus areas: ai, saas, ecommerce, developer, general
await agent.find_project_ideas("Find developer tools opportunities", focus_area="developer")
```

### Evaluation Criteria

Opportunities are scored on:
- **Market Potential** (60% weight): Size and accessibility of target market
- **Implementation Feasibility** (40% weight): Technical complexity and time-to-market

## 🎓 How It Works

1. **Query Processing**: Interprets user requests to understand opportunity types
2. **Strategic Search**: Conducts targeted Reddit searches across relevant subreddits  
3. **Content Analysis**: Extracts pain points using keyword analysis and sentiment detection
4. **Opportunity Evaluation**: Scores potential based on evidence strength and market factors
5. **Recursive Investigation**: Performs follow-up searches for promising opportunities
6. **Report Generation**: Compiles actionable recommendations with supporting evidence

## 📁 Project Structure

```
reddit-idea-finder/
├── src/
│   ├── reddit_idea_finder.py              # Core Reddit search functionality
│   └── reddit_project_idea_finder_agent.py # Main ADK agent implementation
├── dev/
│   ├── test_google_adk_playground.ipynb    # Development and testing notebook
│   └── planner.txt                         # Development planning document
├── demo_agent.py                           # Demo script
├── requirements.txt                        # Python dependencies
├── .env.template                          # Environment variable template
└── README.md                              # This file
```

## 🧪 Testing

The project includes comprehensive testing in the development notebook:

```bash
# Run the Jupyter notebook for interactive testing
jupyter notebook dev/test_google_adk_playground.ipynb

# Or run the demo script
python demo_agent.py
```

## 🛠️ Technical Details

### Built With
- **Google ADK**: Agent orchestration and reasoning
- **PRAW**: Reddit API integration  
- **Python 3.8+**: Core implementation
- **Gemini 2.0 Flash**: Language model for analysis

### Key Components
- `RedditProjectIdeaFinderAgent`: Main agent class with ADK integration
- `search_reddit_for_ideas()`: Tool for discovering Reddit discussions
- `evaluate_business_opportunity()`: Tool for scoring opportunities
- `extract_pain_points()`: Algorithm for identifying user problems

## 🔐 Privacy & Ethics

- Uses Reddit's public API with read-only access
- Respects Reddit's terms of service and rate limits
- Does not store personal user information
- Focuses on publicly available discussions and trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google ADK team for the excellent agent development framework
- Reddit community for providing valuable discussions and insights
- PRAW developers for the robust Reddit API wrapper

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-username/reddit-idea-finder/issues) page
2. Ensure your Reddit API credentials are correctly configured
3. Verify all dependencies are installed: `pip install -r requirements.txt`

---

**Happy opportunity hunting! 🎯**
