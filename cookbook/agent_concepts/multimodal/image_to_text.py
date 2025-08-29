from pathlib import Path

from agno.agent import Agent
from agno.media import Image
from agno.models.ollama import Ollama
from rich.pretty import pprint


agent = Agent(
    model=Ollama(id="llama3.2-vision:11b", host="http://10.20.1.60:11434"),
    markdown=True,
    debug_mode=True,
    show_tool_calls=True,
)



#------ url image
agent.print_response(
    "Write a movie about this image",
    images=[
        # 对于 url 图片，agent 负责下载图片并用base64编码传递给LLM
        Image(
            url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
        )
    ],
    stream=True,
)

#------ local image
image_path = Path(__file__).parent.joinpath("sample.jpg")
agent.print_response(
    "Write a 3 sentence fiction story about the image",
    # 本地图片
    images=[Image(filepath=image_path)],
)

