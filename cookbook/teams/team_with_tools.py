# uv pip install agno agentql wikipedia ddgs


import asyncio
from uuid import uuid4

from agno.agent.agent import Agent
from agno.models.ollama import Ollama
from agno.team import Team
from agno.tools.agentql import AgentQLTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools

wikipedia_agent = Agent(
    name="Wikipedia Agent",
    role="Search wikipedia for information",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[WikipediaTools()],
    instructions=[
        "Find information about the company in the wikipedia",
    ],
    show_tool_calls=True,
    debug_mode=True,
)

website_agent = Agent(
    name="Website Agent",
    role="Search the website for information",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Search the website for information",
    ],
    debug_mode=True,
    show_tool_calls=True,
)

# Define custom AgentQL query for specific data extraction (see https://docs.agentql.com/concepts/query-language)
custom_query = """
{
    title
    text_content[]
}
"""
user_id = str(uuid4())
team_id = str(uuid4())

company_info_team = Team(
    name="Company Info Team",
    mode="coordinate",
    team_id=team_id,
    user_id=user_id,
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    # AgentQLTools 从网页代码中提取出结构化数据, 需要 key
    tools=[ AgentQLTools(api_key="axZeX9iO2QbKnU0AbA-ojZls94WfbJB6M60El1Qpn7P5DCB1dJCQIg" , agentql_query=custom_query)],
    members=[
        wikipedia_agent,
        website_agent,
    ],
    markdown=True,
    instructions=[
        "You are a team that finds information about a company.",
        "First search the web and wikipedia for information about the company.",
        "If you can find the company's website URL, then scrape the homepage and the about page.",
    ],
    show_members_responses=True,
    debug_mode=True,
    show_tool_calls=True,
)

if __name__ == "__main__":
    asyncio.run(
        company_info_team.aprint_response(
            "Write me a full report on everything you can find about Agno, the company building AI agent infrastructure.",
            stream=True,
            stream_intermediate_steps=True,
        )
    )
