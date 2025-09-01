import time
from typing import Any, Callable, Dict
from uuid import uuid4

from agno.agent.agent import Agent
from agno.models.ollama import Ollama
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reddit import RedditTools
from agno.utils.log import logger


def logger_hook(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
    if function_name == "transfer_task_to_member":
        member_id = arguments.get("member_id")
        logger.info(f"Transferring task to member {member_id}")

    # Start timer
    start_time = time.time()
    result = function_call(**arguments)
    # End timer
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"[tool hook] Function {function_name} took {duration:.2f} seconds to execute")
    return result


reddit_agent = Agent(
    name="Reddit Agent",
    agent_id="reddit-agent",
    role="Search reddit for information",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    tools=[RedditTools(cache_results=True)],
    instructions=[
        "Find information about the company on Reddit",
    ],
    tool_hooks=[logger_hook],
    show_tool_calls=True,
    debug_mode=True,
)

website_agent = Agent(
    name="Website Agent",
    agent_id="website-agent",
    role="Search the website for information",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    tools=[DuckDuckGoTools(cache_results=True)],
    instructions=[
        "Search the website for information",
    ],
    tool_hooks=[logger_hook],
    show_tool_calls=True,
    debug_mode=True,
)

user_id = str(uuid4())

company_info_team = Team(
    name="Company Info Team",
    mode="coordinate",
    # 可选, 用于在多用户场景下区分不同的用户
    user_id=user_id,
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    # 可选， 对最终答案的总结。 如果没有该 llm ，则 使用默认的 model
    output_model=Ollama(id="phi4-reasoning:14b",host="http://10.20.1.60:11434"),
    members=[
        reddit_agent,
        website_agent,
    ],
    markdown=True,
    instructions=[
        "You are a team that finds information about a company.",
        "First search the web and wikipedia for information about the company.",
        "If you can find the company's website URL, then scrape the homepage and the about page.",
    ],
    show_members_responses=True,
    tool_hooks=[logger_hook],
    show_tool_calls=True,
    debug_mode=True,
)

if __name__ == "__main__":
    company_info_team.print_response(
        "Write me a brief report on everything you can find about Agno, the company building AI agent infrastructure. the words should be less than 100 words.",
        stream=True,
    )
