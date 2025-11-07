import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

from tavily import TavilyClient

from reddit_idea_finder import RedditIdeaFinder

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# tools
def search_reddit(
    query: str,
    subreddit_name: str = "all",
    sort: Literal["relevance", "hot", "top", "new", "comments"] = "relevance",
    time_filter: Literal["all", "day", "hour", "month", "week", "year"] = "all",
    limit: int = 25,
    include_comments: bool = False,
    max_comments: int = 5,
    comment_limit_more: int = 2,
):
    """Search reddit for posts and comments related to a query.

    """
    finder = RedditIdeaFinder()
    return finder.search_posts(query, subreddit_name=subreddit_name, sort=sort, time_filter=time_filter, limit=limit,
                                include_comments=include_comments, max_comments=max_comments, comment_limit_more=comment_limit_more)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

if __name__ == "__main__":
    # test_results = search_reddit("artificial intelligence", subreddit_name="technology", sort="new", time_filter="month", limit=3, include_comments=True, max_comments=3)
    # print(test_results)
    search_results = internet_search("artificial intelligence", max_results=3, topic="general", include_raw_content=False)
    print(search_results)
    pass