from agno.agent import Agent
from agno.models.ollama.chat import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

reasoning_agent = Agent(
    model=Ollama(id="qwen3:8b", host="http://10.20.1.60:11434"),
    tools=[
        # 给模型提供 reason 规划的 tool， 该 tool 完全内部实现的推理工具，不依赖任何外部服务
        ReasoningTools(
            think=True,
            analyze=True,
            add_instructions=True,
            add_few_shot=True,
        ),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    instructions="Use tables where possible",
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
)
reasoning_agent.print_response(
    "Write a report comparing NVDA to TSLA",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True,
)
