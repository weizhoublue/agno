import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow.v2.step import Step
from agno.workflow.v2.steps import Steps
from agno.workflow.v2.workflow import Workflow
from agno.models.ollama import Ollama

# Define agents for different tasks
researcher = Agent(
    name="Research Agent",
    model=Ollama(id="qwen2.5:7b",host="http://10.20.1.60:11434"),
    tools=[DuckDuckGoTools()],
    instructions="Research the given topic and provide key facts and insights.",
)

writer = Agent(
    name="Writing Agent",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    instructions="Write a comprehensive article based on the research provided. Make it engaging and well-structured.",
)

editor = Agent(
    name="Editor Agent",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    instructions="Review and edit the article for clarity, grammar, and flow. Provide a polished final version.",
)

# Define individual steps
research_step = Step(
    name="research",
    agent=researcher,
    description="Research the topic and gather information",
)

writing_step = Step(
    name="writing",
    agent=writer,
    description="Write an article based on the research",
)

editing_step = Step(
    name="editing",
    agent=editor,
    description="Edit and polish the article",
)

# Create a Steps sequence that chains these above steps together
article_creation_sequence = Steps(
    name="article_creation",
    description="Complete article creation workflow from research to final edit",
    steps=[research_step, writing_step, editing_step],
)

# Create and use workflow
if __name__ == "__main__":
    article_workflow = Workflow(
        name="Article Creation Workflow",
        description="Automated article creation from research to publication",
        steps=[article_creation_sequence],
        debug_mode=True,
    )

    asyncio.run(
        article_workflow.aprint_response(
            message="Write an article about the benefits of renewable energy. the words should be less than 100",
            markdown=True,
        )
    )
