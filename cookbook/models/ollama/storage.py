"""Run `pip install duckduckgo-search sqlalchemy ollama` to install dependencies."""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.postgres import PostgresStorage
from agno.tools.duckduckgo import DuckDuckGoTools

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agent = Agent(
    model=Ollama(id="llama3.1:8b"),
    # 将 Agent 的会话数据存储到 PostgreSQL 数据库中
    # Agent 重启后可以从数据库恢复之前的对话历史和状态
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    tools=[DuckDuckGoTools()],
    # 是否将历史对话消息（获取最近 num_history_runs 次运行的消息）添加到发送给模型的消息列表中。 add_history_to_messages 的默认值是 false
    # 默认包含最近 3 次运行的历史消息（由 num_history_runs 控制）
    add_history_to_messages=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")
