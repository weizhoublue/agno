import json
from textwrap import dedent

import httpx
from agno.agent import Agent
from agno.models.openai import OpenAIChat


def get_upcoming_spacex_launches(num_launches: int = 5) -> str:
    url = "https://api.spacexdata.com/v5/launches/upcoming"
    launches = httpx.get(url).json()
    launches = sorted(launches, key=lambda x: x["date_unix"])[:num_launches]
    return json.dumps(launches, indent=4)


# Create an Agent that has access to real-time SpaceX data
agent = Agent(
    model=OpenAIChat(id="gpt-4.1"),
    # 在运行时，会动态运行 函数 get_upcoming_spacex_launches， context 动态生成了 upcoming_spacex_launches 的 value 
    context={"upcoming_spacex_launches": get_upcoming_spacex_launches},
    # context 中的数据 可以替换如下中的 占位符 
    description=dedent("""\
        You are a cosmic analyst and spaceflight enthusiast. 🚀

        Here are the next SpaceX launches:
        {upcoming_spacex_launches}\
    """),
    # add_state_in_messages will make the `upcoming_spacex_launches` variable
    # available in the description and instructions
    add_state_in_messages=True,
    markdown=True,
)

agent.print_response(
    "Tell me about the upcoming SpaceX missions.",
    stream=True,
)
