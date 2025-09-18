# Quick Setup Guide for Reddit Project Idea Finder

## Overview
The Reddit Project Idea Finder Agent analyzes Reddit discussions to discover profitable business opportunities with supporting evidence links.

## Prerequisites

### 1. Install Required Packages
```bash
pip install google-adk praw python-dotenv
```

### 2. Set Up API Credentials

Create a `.env` file in your project root with:

```env
# Reddit API Credentials (get from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_client_secret

# Google AI API Key (get from https://ai.google.dev/)
GOOGLE_API_KEY=your_google_api_key
```

### 3. Get Reddit API Credentials
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Copy the client ID and secret to your `.env` file

### 4. Get Google AI API Key
1. Go to https://ai.google.dev/
2. Get an API key for Gemini
3. Add it to your `.env` file

## Simple Usage Examples

### Basic Usage (Easiest)
```python
python basic_usage.py
```

### Advanced Examples with Multiple Options
```python
python simple_usage_example.py
```

### Focus on Evidence Links Collection
```python
python evidence_links_example.py
```

### Command Line Usage
```python
python basic_usage.py "Find AI startup ideas for developers"
```

## What You'll Get

Each analysis provides:
- **Business Opportunity Scores** - Market potential and feasibility ratings
- **Supporting Reddit Links** - Organized by category (pain points, opportunities, evidence)
- **Implementation Guidance** - Next steps and risk factors  
- **Target Market Analysis** - User segments and monetization strategies
- **Evidence-Based Recommendations** - Backed by real Reddit discussions

## Example Output Categories

### 🔥 High-Priority Discussions
Most upvoted and discussed posts with strong community engagement

### 😤 Pain Points & Problems  
Posts highlighting specific user frustrations and unmet needs

### 💡 Business Opportunities
Discussions suggesting potential solutions and market gaps

### 📊 Supporting Evidence
Additional posts and comments that validate the opportunities

## File Outputs

The scripts automatically save results in multiple formats:
- `idea_analysis_[timestamp].json` - Full analysis data
- `evidence_links_[timestamp].json` - Structured evidence links
- `evidence_report_[timestamp].md` - Readable markdown report

## Tips for Better Results

1. **Be Specific**: Instead of "startup ideas", try "SaaS tools for small business accounting"

2. **Focus on Problems**: Ask about pain points, frustrations, and unmet needs

3. **Target Markets**: Specify who you want to serve (developers, small businesses, etc.)

4. **Time-Based**: Look for recent trends and emerging problems

## Example Queries That Work Well

```
"Find AI automation opportunities that small businesses desperately need"
"What developer productivity tools are people requesting on Reddit?"  
"Discover e-commerce problems merchants complain about most"
"Find content creation pain points that could become profitable SaaS tools"
"What remote work frustrations could be solved with simple apps?"
```

## Troubleshooting

### Reddit API Issues
- Check your `.env` file has correct credentials
- Verify Reddit app is configured as "script" type
- Make sure you have Reddit account permissions

### Google AI API Issues  
- Verify your API key is active
- Check you have quota remaining
- Ensure the key has Gemini access

### Import Errors
- Make sure all packages are installed: `pip install google-adk praw python-dotenv`
- Check that `src/` directory contains the agent files
- Verify Python path includes the `src` directory

## Next Steps

1. Run `basic_usage.py` for your first analysis
2. Try the example queries to see how it works
3. Experiment with your own specific queries
4. Review the evidence links to validate opportunities
5. Use the business scores to prioritize which ideas to pursue

Happy opportunity hunting! 🚀