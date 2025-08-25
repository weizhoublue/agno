from typing import List

from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama
from pydantic import BaseModel, Field
from rich.pretty import pprint  # noqa


# 一个继承自 BaseModel 的 Pydantic 类
class MovieScript(BaseModel):
    name: str = Field(..., description="Give a name to this movie")
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


# Agent that returns a structured output
structured_output_agent = Agent(
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    description="You write movie scripts.",
    # 当设置了 response_model 后，Agent 会将模型的响应解析为指定的 Pydantic 模型格式，而不是返回普通的字符串内容
    # 需要一个继承自 BaseModel 的 Pydantic 类
    # agent 会根据您的 Pydantic 模型自动生成详细的 JSON 格式说明，作为 llm 的系统提示词
    response_model=MovieScript,
)

# Get the response in a variable
# json_mode_response: RunResponse = json_mode_agent.run("New York")
# pprint(json_mode_response.content)
# structured_output_response: RunResponse = structured_output_agent.run("New York")
# pprint(structured_output_response.content)


# Run the agent
structured_output_agent.print_response("New York")
# ┃ {                                                                                                                                                                             ┃
# ┃   "name": "City of Dreams",                                                                                                                                                   ┃
# ┃   "setting": "New York City, New York",                                                                                                                                       ┃
# ┃   "ending": "bittersweet",                                                                                                                                                    ┃
# ┃   "genre": "Drama",                                                                                                                                                           ┃
# ┃   "characters": [                                                                                                                                                             ┃
# ┃     "Jack Harris: A struggling artist in his late twenties.",                                                                                                                 ┃
# ┃     "Sarah Taylor: A successful businesswoman in her mid-thirties.",                                                                                                          ┃
# ┃     "Mike Thompson: A charming but untrustworthy entrepreneur."                                                                                                               ┃
# ┃   ],                                                                                                                                                                          ┃
# ┃   "storyline": "In the city that never sleeps, Jack Harris is trying to make a name for himself as an artist. Meanwhile, Sarah Taylor has it all - wealth, status, and a sens ┃
# ┃ }                                                                                                                                                                             ┃
