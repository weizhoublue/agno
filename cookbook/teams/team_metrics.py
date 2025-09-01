from typing import Iterator

from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools
from agno.utils.pprint import pprint_run_response
from rich.pretty import pprint

stock_searcher = Agent(
    name="Stock Searcher",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    role="Searches the web for information on a stock.",
    tools=[YFinanceTools()],
)

team = Team(
    name="Stock Research Team",
    mode="route",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    members=[stock_searcher],
    markdown=True,
    debug_mode=True,
    show_members_responses=True,
)


run_stream: Iterator[RunResponse] = team.run(
    "What is the stock price of NVDA", stream=True
)
pprint_run_response(run_stream, markdown=True)


print("---" * 5, "Team Leader Message Metrics", "---" * 5)
# Print metrics per message for lead agent
if team.run_response.messages:
    for message in team.run_response.messages:
        if message.role == "assistant":
            if message.content:
                print(f"Message: {message.content}")
            elif message.tool_calls:
                print(f"Tool calls: {message.tool_calls}")
            print("---" * 5, "Metrics", "---" * 5)
            pprint(message.metrics)
            print("---" * 20)


# Print the metrics
print("---" * 5, "Aggregated Metrics of Team Agent", "---" * 5)
pprint(team.run_response.metrics)

# Print the session metrics
print("---" * 5, "Session Metrics", "---" * 5)
pprint(team.session_metrics)

"""
--------------- Session Metrics ---------------
SessionMetrics(
│   input_tokens=495,
│   output_tokens=155,
│   total_tokens=650,
│   audio_tokens=0,
│   input_audio_tokens=0,
│   output_audio_tokens=0,
│   cached_tokens=0,
│   cache_write_tokens=0,
│   reasoning_tokens=0,
│   prompt_tokens=0,
│   completion_tokens=0,
│   prompt_tokens_details=None,
│   completion_tokens_details=None,
│   additional_metrics={'total_duration': 19616374099, 'load_duration': 16607629080, 'prompt_eval_duration': 437245506, 'eval_duration': 2556073262},
│   time=19.75362687499728,
│   time_to_first_token=17.130575374991167,
│   timer=None
)
"""

print("---" * 5, "Team Member Message Metrics 每一个成员的消息指标", "---" * 5)
# Print metrics per member per message
if team.run_response.member_responses:
    for member_response in team.run_response.member_responses:
        if member_response.messages:
            for message in member_response.messages:
                if message.role == "assistant":
                    if message.content:
                        print(f"Message: {message.content}")
                    elif message.tool_calls:
                        print(f"Tool calls: {message.tool_calls}")
                    print("---" * 5, "Metrics", "---" * 5)
                    pprint(message.metrics)
                    print("---" * 20)


# Print the session metrics
print("---" * 5, "Full Team Session Metrics 总体的会话指标", "---" * 5)
pprint(team.full_team_session_metrics)

"""
--------------- Full Team Session Metrics ---------------
SessionMetrics(
│   input_tokens=1044,
│   output_tokens=309,
│   total_tokens=1353,
│   audio_tokens=0,
│   input_audio_tokens=0,
│   output_audio_tokens=0,
│   cached_tokens=0,
│   cache_write_tokens=0,
│   reasoning_tokens=0,
│   prompt_tokens=0,
│   completion_tokens=0,
│   prompt_tokens_details=None,
│   completion_tokens_details=None,
│   additional_metrics={'total_duration': 643214994, 'load_duration': 197034647, 'prompt_eval_duration': 75612074, 'eval_duration': 313441741},
│   time=37.28606516699074,
│   time_to_first_token=17.130575374991167,
│   timer=None
)
"""