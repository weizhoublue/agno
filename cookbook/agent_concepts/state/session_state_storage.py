"""Run `pip install agno openai sqlalchemy` to install dependencies."""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.sqlite import SqliteStorage


# Define a tool that adds an item to the shopping list
def add_item(agent: Agent, item: str) -> str:
    # 如下这行，会作为本 tool 的描述，告诉 llm 可以调用本 tool
    """Add an item to the shopping list."""
    if item not in agent.session_state["shopping_list"]:
        agent.session_state["shopping_list"].append(item)
    return f"The shopping list is now {agent.session_state['shopping_list']}"


agent = Agent(
    model=Ollama(id="phi4-mini:3.8b",host="http://10.20.1.60:11434"),
    session_id="fixed_id_for_demo",
    # 初始化 session state
    session_state={"shopping_list": []},
    # 【可选】session state 数据进行持久化。否则 存储在内存中
    storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/data.db"),
    # 添加一个 tool， 用于自动向 session state 中添加购物清单项目
    tools=[add_item],
    # 将 session state 中的购物清单添加到 instructions 中
    instructions="Current shopping list is: {shopping_list}",
    # Important: Set `add_state_in_messages=True`
    # to make `{shopping_list}` available in the instructions
    add_state_in_messages=True,
    markdown=True,
    debug_mode=True,
)

# Example usage
agent.print_response(
    "What's on my shopping list?",
    stream=True,
)
print(f"Session state: {agent.session_state}")

# 这次对话，Agent 工具用户的指示，自动调用了 add_item tool，把 milk, eggs, bread 添加到 session state 中
agent.print_response(
    "Add milk, eggs, and bread",
    stream=True,
)
print(f"Session state: {agent.session_state}")


