from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.sqlite import SqliteStorage


# Define tools to manage our shopping list
def add_item(agent: Agent, item: str) -> str:
    """Add an item to the shopping list and return confirmation."""
    # Add the item if it's not already in the list
    if item.lower() not in [i.lower() for i in agent.session_state["shopping_list"]]:
        agent.session_state["shopping_list"].append(item)
        return f"Added '{item}' to the shopping list"
    else:
        return f"'{item}' is already in the shopping list"


def remove_item(agent: Agent, item: str) -> str:
    """Remove an item from the shopping list by name."""
    # Case-insensitive search
    for i, list_item in enumerate(agent.session_state["shopping_list"]):
        if list_item.lower() == item.lower():
            agent.session_state["shopping_list"].pop(i)
            return f"Removed '{list_item}' from the shopping list"

    return f"'{item}' was not found in the shopping list"


def list_items(agent: Agent) -> str:
    """List all items in the shopping list."""
    shopping_list = agent.session_state["shopping_list"]

    if not shopping_list:
        return "The shopping list is empty."

    items_text = "\n".join([f"- {item}" for item in shopping_list])
    return f"Current shopping list:\n{items_text}"


# Create a Shopping List Manager Agent that maintains state
agent = Agent(
    # 注意，模型对工具支持很重要，否则不会调用 tool 来更新我们的 session state
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    # 初始化 session state 中的数据， 它是个我们任意定义的 json 数据
    session_state={"shopping_list": []},
    # 给 llm 添加 tool， 用于自动向 session state 中添加/删除数据
    tools=[add_item, remove_item, list_items],
    # 可以在 instructions 中使用 session state 中的数据进行占位符替换
    instructions=dedent("""\
        Your job is to manage a shopping list.

        The shopping list starts empty. You can add items, remove items by name, and list all items.

        Current shopping list: {shopping_list}
    """),
    add_state_in_messages=True,
    # 【可选】session state 数据进行持久化。否则 存储在内存中
    # storage=SqliteStorage(table_name="shopping_list", db_file="tmp/data.db"),
    markdown=True,
    debug_mode=True,
)


# 以下这些对话，Agent 根据 用户的指示，自动调用了 tool 对 session state 中的数据进行修改
agent.print_response("Add milk, eggs, and bread to the shopping list", stream=True)
print(f"Session state: {agent.session_state}")

agent.print_response("I got bread", stream=True)
print(f"Session state: {agent.session_state}")

agent.print_response("I need apples and oranges", stream=True)
print(f"Session state: {agent.session_state}")

agent.print_response("whats on my list?", stream=True)
print(f"Session state: {agent.session_state}")

agent.print_response(
    "Clear everything from my list and start over with just bananas and yogurt",
    stream=True,
)
print(f"Session state: {agent.session_state}")
