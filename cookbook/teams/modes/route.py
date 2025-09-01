"""
 
"""

import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.team.team import Team

english_agent = Agent(
    name="English Agent",
    role="You only answer in English",
    model= Ollama(id="mistral-small3.2:24b",host="http://10.20.1.60:11434"),
    debug_mode=True,
)
 
chinese_agent = Agent(
    name="Chinese Agent",
    role="You only answer in Chinese",
    model= Ollama(id="mistral-small3.2:24b",host="http://10.20.1.60:11434"),
    debug_mode=True,
)

multi_language_team = Team(
    name="Multi Language Team",
    # 这会让 team llm 的系统提示词中，明确只选一个 member 来干活 
    mode="route",
    model= Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    members=[
        english_agent,
        chinese_agent,
    ],
    markdown=True,
    instructions=[
        "You are a language router that directs questions to the appropriate language agent.",
        "If the user asks in a language whose agent is not a team member, respond in English with:",
        "'I can only answer in the following languages: English, Chinese. Please ask your question in one of these languages.'",
        "Always check the language of the user's input before routing to an agent.",
        "For unsupported languages like Korean, respond in English with the above message.",
    ],
    show_members_responses=True,
    debug_mode=True,
    show_tool_calls=True,
)


if __name__ == "__main__":
    # Ask "How are you?" in all supported languages
    asyncio.run(multi_language_team.aprint_response(
        "How are you?", stream=True  # English
    ))

    asyncio.run(multi_language_team.aprint_response(
        "你好吗？", stream=True  # Chinese
    ))

