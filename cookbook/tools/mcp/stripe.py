
import asyncio
import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.mcp import MCPTools
from agno.utils.log import log_error, log_exception, log_info
#from agno.models.deepseek import DeepSeek
#from agno.models.litellm import LiteLLM

async def run_agent(message: str) -> None:
    npx_command = "npx.cmd" if os.name == "nt" else "npx"
    try:
        # Initialize MCP toolkit with Stripe server
        async with MCPTools(
            command=f"{npx_command} -y @larksuiteoapi/lark-mcp mcp -a cli_a83032681b53901c -s OKkKQMPJoQeYI7LpimPVtcU6Kensyj4l --oauth"
        ) as feishu_mcp:
            agent = Agent(
                name="StripeAgent",
                model=Ollama(id="qwen3:14b", host="http://10.20.1.60:11434"),
                #model=DeepSeek(id="deepseek-chat"),
                #model=LiteLLM( id="gpt-4o", api_base="http://10.20.1.20:4000"),
                instructions=dedent("""\
                   - 使用 feishu_mcp tool， 基于用户的邮箱地址，能够给任何用户发送消息。
                     可通过 feishu_mcp 的 im.v1.message.create 方法发送消息，采用邮箱的格式如下
                     im_v1_message_create(data={'content': '{"text":"hello"}', 'msg_type': 'text', 'receive_id': 'weizhou.lan@daocloud.io'}, params={'receive_id_type': 'email'})
                """),
                tools=[feishu_mcp],
                markdown=True,
                show_tool_calls=True,
            )

            # Run the agent with the provided task
            log_info(f"Running agent with assignment: '{message}'")
            await agent.aprint_response(message, stream=True)

    except FileNotFoundError:
        error_msg = f"Error: '{npx_command}' command not found. Please ensure Node.js and npm/npx are installed and in your system's PATH."
        log_error(error_msg)
    except Exception as e:
        log_exception(f"An unexpected error occurred during agent execution: {e}")


if __name__ == "__main__":
    task = "给邮箱是 weizhou.lan@daocloud.io 的用户发送一个 “你好！” 的消息"
    asyncio.run(run_agent(task))

