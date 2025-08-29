"""
uv pip install ddgs agno
"""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger  

from typing import Any, Callable, Dict

def logger_hook(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
    # Pre-hook logic: this runs before the tool is called
    logger.info(f"------ [tool hook] Running {function_name} with arguments {arguments}")

    # Call the tool
    result = function_call(**arguments)

    # Post-hook logic: this runs after the tool is called
    logger.info(f"------ [tool hook] Result of {function_name} is {result}")
    return result


agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    tools=[
        DuckDuckGoTools(
            #【可选】
            exclude_tools=[],
            include_tools=["duckduckgo_news"],
            # 【可选】当列表中指定的工具被调用后，Agent 会立即把结果返回给用户，停止当前对话，不会继续处理后续的响应或工具调用
            stop_after_tool_call_tools=["duckduckgo_news"],
            # 【可选】当列表中指定的工具被调用后，其执行结果会显示给用户，而不仅仅是传递给模型
            show_result_tools=["duckduckgo_news"],
            # 【可选】缓存工具调用结果，避免重复调用
            cache_results=True,
        )
    ],
    # 【可选】限制的是单次 Agent 运行中的工具调用次数，而不是整个 Agent 实例的总调用次数。 默认是 None， 即没有限制。
    # 设置该上限，能够有效避免 llm 无限制的 调用 tool 进行循环， 浪费 token
    tool_call_limit=1,
    # 【可选，没测试成功】工具调用钩子， 可以在工具调用前、后执行自定义逻辑。实现调试、校验 等目的 
    tool_hooks=[logger_hook],
    show_tool_calls=True,
    debug_mode=True,
)


agent.print_response("Whats the latest about gpt 4.5?", stream=True, markdown=True)


