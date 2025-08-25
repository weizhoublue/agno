"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    # DuckDuckGoTools 是一个免费的网络搜索工具，可以直接使用而无需任何 API 密钥配置
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?")
