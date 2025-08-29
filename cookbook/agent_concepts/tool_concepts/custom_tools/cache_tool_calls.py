import json
from typing import Iterator

import httpx
from agno.agent import Agent
from agno.tools import tool


# 【可选】通过 @tool 修饰符，可以定义 tool 级别的 工作参数  https://docs.agno.com/tools/tool-decorator#%40tool-parameters-reference
#    - 当 cache_results=True 时，如果工具调用的入参与之前某一次的缓存场景下完全相同，就会使用那一次的缓存结果
@tool(show_result=True, stop_after_tool_call=True, cache_results=True)
def get_top_hackernews_stories(num_stories: int = 5) -> str:
    # Fetch top story IDs
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


agent = Agent(
    tools=[get_top_hackernews_stories],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
)
agent.print_response("What are the top hackernews stories?", stream=True)
