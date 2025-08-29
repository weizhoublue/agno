"""Show how to decorate a custom hook with a tool execution hook."""

import json
import time
from typing import Any, Callable, Dict, Iterator

import httpx
from agno.agent import Agent
from agno.tools import tool
from agno.utils.log import logger
from agno.models.ollama import Ollama

#--------------------

# 定义一个 tool 的执行回调，实现 debug、统计等功能
def duration_logger_hook(
    function_name: str, function_call: Callable, arguments: Dict[str, Any]
):
    """Log the duration of the function call"""
    start_time = time.time()

    result = function_call(**arguments)

    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"[tool hook]Function {function_name} took {duration:.2f} seconds to execute")
    return result


# tool 函数，没有方法调用参数 
# 入参代表了方法调用的入参，特殊的是，可以带 或 不带 agent: Agent 参数，它不算入工具调用的入参，它用于获取 agent 对象
# 【可选】通过 @tool 修饰符，可以定义 tool 级别的 工作参数  https://docs.agno.com/tools/tool-decorator#%40tool-parameters-reference
#    - 当 cache_results=True 时，如果工具调用的入参与之前某一次的缓存场景下完全相同，就会使用那一次的缓存结果
@tool(
    tool_hooks=[duration_logger_hook], 
    cache_results=True,
)
def get_top_funystories(agent: Agent) -> Iterator[str]:
    """Get the top funny stories from Hacker News."""    
    num_stories = agent.context.get("num_stories", 5) if agent.context else 5

    # Fetch top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    final_stories = {}
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        final_stories[story_id] = story

    return json.dumps(final_stories)

#--------------------

# 带有 方法调用参数 的 tool
# 入参代表了方法调用的入参， 特殊的是，可以带 或 不带 agent: Agent 参数，它不算入工具调用的入参，用于获取 agent 对象
@tool(
    show_result=True, 
    cache_results=True,
)
def get_top_sad_stories(num_stories: int = 5) -> str:
    """Get the top sad stories from Hacker News."""    
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # Yield story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        stories.append(json.dumps(story))

    return "\n".join(stories)

#-------------

agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    context={
        "num_stories": 2,
    },
    tools=[ get_top_funystories , get_top_sad_stories ],
    markdown=True,
    show_tool_calls=True,
    #debug_mode=True,
)


agent.print_response("What are the top interesting hackernews stories?", stream=True)


