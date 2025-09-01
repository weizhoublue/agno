"""
 
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools

reddit_researcher = Agent(
    name="Reddit Researcher",
    role="Research a topic on Reddit",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),
    debug_mode=True,
)

hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    role="Research a topic on HackerNews.",
    tools=[HackerNewsTools()],
    add_name_to_instructions=True,
    instructions=dedent("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
    debug_mode=True,
)


agent_team = Team(
    name="Discussion Team",
    mode="collaborate",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    members=[
        reddit_researcher,
        hackernews_researcher,
    ],
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    success_criteria="The team has reached a consensus.",
    enable_agentic_context=True,
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
    debug_mode=True,
)

if __name__ == "__main__":
    asyncio.run(
        agent_team.aprint_response(
            message="Start the discussion on the topic: 'What is the best way to learn to code?'",
            stream=True,
            stream_intermediate_steps=True,
        )
    )
