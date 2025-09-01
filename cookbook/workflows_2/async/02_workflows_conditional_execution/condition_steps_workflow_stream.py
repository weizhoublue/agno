import asyncio

from agno.agent.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow.v2.condition import Condition
from agno.workflow.v2.step import Step
from agno.workflow.v2.types import StepInput
from agno.workflow.v2.workflow import Workflow
from agno.models.ollama import Ollama

# === BASIC AGENTS ===
researcher = Agent(
    model=Ollama(id="mistral-small3.2:24b",host="http://10.20.1.60:11434"),
    name="Researcher",
    instructions="Research the given topic and provide detailed findings.",
    tools=[DuckDuckGoTools()],
)

summarizer = Agent(
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    name="Summarizer",
    instructions="Create a clear summary of the research findings.",
)

fact_checker = Agent(
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    name="Fact Checker",
    instructions="Verify facts and check for accuracy in the research.",
    tools=[DuckDuckGoTools()],
)

writer = Agent(
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    name="Writer",
    instructions="Write a comprehensive article based on all available research and verification.",
)

# === CONDITION EVALUATOR ===


def needs_fact_checking(step_input: StepInput) -> bool:
    """Determine if the research contains claims that need fact-checking"""
    summary = step_input.previous_step_content or ""

    # Look for keywords that suggest factual claims
    fact_indicators = [
        "study shows",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]

    return any(indicator in summary.lower() for indicator in fact_indicators)


# === WORKFLOW STEPS ===
research_step = Step(
    name="research",
    description="Research the topic",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="Summarize research findings",
    agent=summarizer,
)

# Conditional fact-checking step
fact_check_step = Step(
    name="fact_check",
    description="Verify facts and claims",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="Write final article",
    agent=writer,
)

# === BASIC LINEAR WORKFLOW ===
basic_workflow = Workflow(
    name="Basic Linear Workflow",
    description="Research -> Summarize -> Condition(Fact Check) -> Write Article",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="Check if fact-checking is needed",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
    debug_mode=True,
)

if __name__ == "__main__":
    print("🚀 Running Basic Linear Workflow Example")
    print("=" * 50)

    try:
        asyncio.run(
            basic_workflow.aprint_response(
                message="Recent breakthroughs in quantum computing",
                stream=True,
                stream_intermediate_steps=True,
            )
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
