from tools import internet_search, search_reddit

from deepagents import create_deep_agent


# Prompt prefix to steer the agent to be an expert researcher
research_instructions = """You are an expert reddit researcher. Your job is to find out what people are saying about a topic on reddit.

# You have access to a few tools.
- `search_reddit`
Search reddit for posts and comments related to a query, with options to filter by subreddit, sort order, time, and include comments.

- `internet_search`
Run a web search using Tavily search engine with configurable max results, topic category, and content options.
It is useful to find relevant subreddits to search in reddit.

# instructions:
First use internet_search to find and list top 10 most related and popular subreddits to the user's query.
Then make reddit searches (as many as required up to 3) in those subreddits (by calling the tool with subreddit_name=subreddit_1+subreddit_2+subreddit_3+...) and the right queries to gather all the posts and related comments.
Try to find the most recent results (max 3 months old) and include comments in the search results.

Final answer should be a comprehensive answer to the user's question, based on your findings, with references to the sources you used.
"""

# Create the agent
agent = create_deep_agent(
    [internet_search, search_reddit],
    research_instructions,
    model="azure_openai:gpt-4.1",
)

if __name__ == "__main__":
    # Invoke the agent
    result = agent.invoke({"messages": [{"role": "user", "content": "what are people talking about in SaaS community?"}]})
    print(result)