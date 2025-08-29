"""
uv pip install ddgs agno
"""

import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[DuckDuckGoTools(cache_results=True), YFinanceTools(cache_results=True)],
    show_tool_calls=True,
    debug_mode=True,
)

asyncio.run(
    agent.aprint_response(
        "What is the current stock price of AAPL and latest news on 'Apple'?",
        markdown=True,
    )
)
