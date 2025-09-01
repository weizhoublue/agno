from agno.agent import Agent
from agno.memory.agent import AgentMemory
from agno.memory.db.postgres import PgMemoryDb
from agno.models.ollama import Ollama
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.storage.postgres import PostgresStorage


basic_agent = Agent(
    name="Basic Agent",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True,
)

playground = Playground(
    agents=[
        basic_agent,
    ],
    name="Basic Agent",
    description="A playground for basic agent",
    app_id="basic-agent",
)


#  发现 网站打开后 failed to load endpoint
#app = playground.get_app()
# 使用空前缀或指定前缀 成功打开访问。 否则发现 网站打开后 failed to load endpoint
app = playground.get_app(prefix="")  
if __name__ == "__main__":
    # Start the playground server
    playground.serve(
        # 是一个模块路径字符串，告诉 uvicorn 从哪里导入 FastAPI 应用实例
        # 从 basic.py 中的变量 app 导入
        app="basic:app",
        host="localhost",
        port=7777,
        reload=True,
    )
