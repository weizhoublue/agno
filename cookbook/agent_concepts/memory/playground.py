"""
uv venv
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
uv pip install agno ollama duckduckgo-search

运行后，务必使用 firefox 或者 chrome 来打开日志中出现的地址
┃  Playground URL: https://app.agno.com/playground?endpoint=xxxxx  ┃

"""

from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.ollama import Ollama
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools

# Database file for memory and storage
db_file = "tmp/playground.db"

# Initialize memory.v2
memory = Memory(
    # Use any model for creating memories
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
    delete_memories=True,
    clear_memories=True,
)
# Initialize storage
storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)

# Initialize Agent
agent = Agent(
    name="Memory Agent",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    # Store memories in a database
    memory=memory,
    # Give the Agent the ability to update memories
    enable_agentic_memory=True,
    # Store the chat history in the database
    storage=storage,
    # Add chat history to the messages
    add_history_to_messages=True,
    num_history_runs=3,
    # Give the agent a tool to access chat history
    read_chat_history=True,
    # Add datetime to the instructions
    add_datetime_to_instructions=True,
    # Use markdown for the response
    markdown=True,
    # Add a tool to search the web
    tools=[DuckDuckGoTools()],
)


playground = Playground(
    agents=[
        agent,
    ],
    app_id="memory-playground-app",
    name="Memory Playground",
)

#  发现 网站打开后 failed to load endpoint
#app = playground.get_app()
# 使用空前缀或指定前缀 成功打开访问。 否则发现 网站打开后 failed to load endpoint
app = playground.get_app(prefix="")  

if __name__ == "__main__":
    # Start the playground server
    playground.serve(
        app="playground:app",
        host="localhost",
        port=7777,
        reload=True,
    )
