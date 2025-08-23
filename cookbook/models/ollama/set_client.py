"""Run `pip install yfinance` to install dependencies."""

from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama
from ollama import Client as OllamaClient

agent = Agent(
    model=Ollama(id="llama3.1:8b", 
                # 允许您直接传入一个预配置的 Ollama 客户端实例，而不是让模型自动创建客户端
                client=OllamaClient()),
    markdown=True,
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")
