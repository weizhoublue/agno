import random

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import tool


@tool(show_result=True, stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    # In a real implementation, this would call a weather API
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    random_weather = random.choice(weather_conditions)

    return f"The weather in {city} is {random_weather}."


agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    markdown=True,
)
agent.print_response("What can you do?", stream=True)

# tool 可以被动态 按需 添加
agent.add_tool(get_weather)
agent.print_response("What is the weather in San Francisco?", stream=True)
