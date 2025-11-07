from threading import current_thread
import uuid

from litellm import aget_assistants

from tools import internet_search, search_reddit
from prompts import business_research_instructions, generic_reddit_research_prompt
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

class ModelOptions:
   GPT_4_1 = "azure_openai:gpt-4.1"
   GPT_4O = "azure_openai:gpt-4o"
   GPT_5_CHAT = "azure_openai:gpt-5-chat"
   GPT_5_MINI = "azure_openai:gpt-5-mini"
   O4_MINI = "azure_openai:o4-mini"
   O4_MINI = "azure_openai:grok-4-fast-reasoning"
   GEMINI_2_5_FLASH = "google_genai:gemini-2.5-flash"
   GEMINI_2_5_PRO = "google_genai:gemini-2.5-pro"

def generate_thread_id():
    return str(uuid.uuid4())

def create_agent(system_prompt: str, tools: list, model: str = ModelOptions.GPT_4_1, add_memory: bool = True, debug: bool = False):
   # Create the agent
   agent = create_deep_agent(
      tools=tools,
      system_prompt=system_prompt,
      model=model,
      debug=debug
   )
   if add_memory:
      checkpointer = InMemorySaver()
      agent.checkpointer = checkpointer
   return agent


def create_reddit_idea_finder_agent(instructions: str = business_research_instructions, model: str = ModelOptions.GPT_4_1, debug: bool = False):
   # Create the agent
   agent = create_agent(
      instructions,
      [internet_search, search_reddit],
      model=model,
      add_memory=True,
      debug=debug,
   )
   return agent


current_thread_id = generate_thread_id()

def query_agent(agent, query: str, thread_id: str = current_thread_id, reset_memory: bool = False):
    if reset_memory or not thread_id:
        thread_id = generate_thread_id()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": thread_id}}
        )
    return result


if __name__ == "__main__":
    # Invoke the agent
    agent = create_reddit_idea_finder_agent()
    result = query_agent(agent, "what are people talking about in SaaS community?")
    print(result)