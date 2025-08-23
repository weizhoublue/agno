from pathlib import Path

from agno.agent import Agent
from agno.media import Image
from agno.models.ollama import Ollama


agent = Agent(
    model=Ollama(id="gemma3:12b",host="http://10.20.1.60:11434"),
    markdown=True,
    # ---- 系统提示词 [可选]
    # [可选] 被放在系统消息的最开头  , 用于做简短的自我描述
    description="you are a helpful assistant",
    # [可选] 放在 <your_goal> 标签中
    # goal = "..."
    # [可选] 放在 <self.role> 标签中, 描述角色的背景和定位
    # role = "..."
    # [可选] 放在 <instructions> 标签中
    instructions=["offer practical and concise advice"],
)



# 同步运行
agent.print_response(
    "Write me python code to solve quadratic equations. Explain your reasoning."
)

 
# 流式输出
# Get the response in a variable
# run_response: Iterator[RunResponseEvent] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)
image_path = Path(__file__).parent.joinpath("super-agents.png")
agent.print_response(
    "what is written in the image",
    images=[Image(filepath=image_path)],
    # 以流式方式实时输出收到的 llm 响应, 模型返回的每个响应块都会被处理并立即传递给用户，而不是等待完整响应 . 
    # 而不是等待 llm 完成后再一次性输出. 能提高交互体验
    # 在 agno 框架中，所有模型都必须实现流式接口
    stream=True,
)


