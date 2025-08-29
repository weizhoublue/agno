from agno.agent import Agent
from agno.models.ollama.chat import Ollama

# 如果配备了 reasoning_model ， 
# agent 第一步 会 使用 推理模型（只调用一次） 分析问题并生成推理结果，
#       第二步，提供 推理模型的响应和用户问题 给基础模型（可能调用多次），让基础模型生成最终答案
# 分离架构提供了几个重要优势：
#   - 推理模型专注于深度分析和逻辑推理，主模型专注于生成高质量的用户响应 
#   - 成本优化：推理模型通常计算成本较高，分离后可以用更经济的模型生成最终响应
agent = Agent(
    model=Ollama(id="llama3.1:latest", host="http://10.20.1.60:11434"),
    reasoning_model=Ollama(id="deepseek-r1:8b", host="http://10.20.1.60:11434"),
    debug_mode=True,
)
agent.print_response(
    "Solve the trolley problem. Evaluate multiple ethical frameworks. "
    "Include an ASCII diagram of your solution.",
    stream=True,
)

