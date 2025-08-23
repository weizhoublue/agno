from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    instructions="Use tables to display data.",
)

agent.print_response("Write a report on NVDA", stream=True, markdown=True)
