from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.ollama import Ollama
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    name="Calculator Evaluation",
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    agent=Agent(
        model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
        tools=[CalculatorTools(enable_all=True)],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=3,
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8
