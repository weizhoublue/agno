"""
Notion MCP Agent - Manages your documents

This example shows how to use the Agno MCP tools to interact with your Notion workspace.

1. Start by setting up a new internal integration in Notion: https://www.notion.so/profile/integrations
2. Export your new Notion key: `export NOTION_API_KEY=ntn_****`
3. Connect your relevant Notion pages to the integration. To do this, you'll need to visit that page, and click on the 3 dots, and select "Connect to integration".

Dependencies: pip install agno mcp openai

Usage:
  python cookbook/tools/mcp/notion_mcp_agent.py
"""

import asyncio
import json
import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters


async def run_agent():


    command = "npx"
    args = ["-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "cli_a83032681b53901c", "-s", "OKkKQMPJoQeYI7LpimPVtcU6Kensyj4l", "--oauth"]
    env = {
        "LARK_DOMAIN": "https://open.feishu.cn"
    }
    server_params = StdioServerParameters(command=command, args=args, env=env)

    async with MCPTools(server_params=server_params) as mcp_tools:
        agent = Agent(
            name="chat",
            model=Ollama(id="qwen3:14b", host="http://10.20.1.60:11434"),
            tools=[mcp_tools],
            description="你是一个聊天客服",
            instructions=dedent("""\
                你能够基于 MCP tools 实现消息发送、获取、更新等操作。
            """),
            markdown=True,
            show_tool_calls=True,
            debug_mode=True,
        )

        await agent.acli_app(
            message="你好，我是客服小明，有什么问题可以找我。",
            stream=True,
            markdown=True,
            exit_on=["exit", "quit"],
        )


if __name__ == "__main__":
    asyncio.run(run_agent())
