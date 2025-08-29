from agno.agent import Agent,RunResponse, RunResponseEvent
from agno.models.ollama import Ollama
from agno.utils.pprint import pprint_run_response
from typing import Iterator
from rich.pretty import pprint

agent = Agent(
    model=Ollama(id="phi4:14b",host="http://10.20.1.60:11434"),
    markdown=True,
    )

#---------- 几种 输出 agent 交互数据的 方式

# 方式 1
# print_response 底层调用了 Agent.run() function ， 并把输出 通时打印到了 终端
agent.print_response( 
        "What is the stock price of Apple?", 
        # 是否要把 llm 的响应 实时 输出，优化输入体验 。 否则 是 一次性输出
        stream=True,
        )

# 方式2 ：markdown 格式打印
# Print the response in markdown format
response: RunResponse = agent.run("Tell me a 5 second short story about a robot")
pprint_run_response(response, markdown=True)

# 方式3：
# Run agent and return the response as a stream
response_stream: Iterator[RunResponseEvent] = agent.run(
    "Tell me a 5 second short story about a lion",
    stream=True,
    stream_intermediate_steps=True,
)
# Print the response stream in markdown format
pprint_run_response(response_stream, markdown=True)


##----------- 打印 agent 详细的 metrics 
# https://docs.agno.com/agents/metrics

# Print metrics per message
if agent.run_response.messages:
    for message in agent.run_response.messages:
        if message.role == "assistant":
            if message.content:
                print(f"Message: {message.content}")
            elif message.tool_calls:
                print(f"Tool calls: {message.tool_calls}")
            print("---" * 5, "Metrics", "---" * 5)
            pprint(message.metrics)
            print("---" * 20)

# Print the aggregated metrics for the whole run
print("---" * 5, "Collected Metrics", "---" * 5)
pprint(agent.run_response.metrics)
# Print the aggregated metrics for the whole session
print("---" * 5, "Session Metrics", "---" * 5)
pprint(agent.session_metrics)




