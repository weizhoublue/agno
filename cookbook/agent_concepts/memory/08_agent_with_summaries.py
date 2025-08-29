"""

uv venv
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
uv pip install agno ollama rich sqlalchemy

"""

from agno.agent.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.memory.v2 import UserMemory
from agno.memory.v2.summarizer import SessionSummarizer
from rich.pretty import pprint
from agno.models.ollama import Ollama
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.storage.postgres import PostgresStorage


from agno.debug import enable_debug_mode
# 启用调试模式
enable_debug_mode()

# 给 memory 配置独立的 LLM
# 当启用 enable_user_memories、SessionSummarizer 、搜索用户记忆、 enable_agentic_memory 时，Memory 需要配置 LLM 进行记忆的分析、提取
# 这里配置了 qwen3:8b    工作正常
# 这里的模型对于 tool 调用很重要，尝试过一些其他模型，都在 memory 使用中有报错日志。当使用 llama3.1 llama3.2 phi4:14b deepseek-r1 都有报错 
memory_model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434")

# 本地文件存储
# memory_db = SqliteMemoryDb(table_name="agent_memory", db_file="tmp/memory.db")
# 对接本地部署的 agnohq/pgvector 容器
db_url="postgresql+psycopg://ai:ai@10.20.1.60:5532/ai"
memory_db=PostgresMemoryDb(table_name="agent_memories", db_url=db_url)

memory = Memory(
            model=memory_model,
            # 使用 本地的 sqlite 进行持久化记忆。如果不配置，这存储在 内存中 
            db=memory_db,
            # 设置 summarizer， 用于对话总结
            summarizer=SessionSummarizer(model=memory_model),
        )

# memory = Memory(
#     db=SqliteMemoryDb(table_name="memory", db_file="tmp/memory.db"),
#     memory_manager=MemoryManager(
#         model=Gemini(id="gemini-2.0-flash-001"),
#         memory_capture_instructions=dedent("""\
#             Memories should only include details about the user's academic interests.
#             Ignore names, hobbies, and personal interests.
#             """),
#     ),
# )

# Reset the memory for this example
# 清空内存和持久化存储中的所有记忆数据
memory.clear()

# 我们可以添加一些用户记忆
memory.add_user_memory(
    memory=UserMemory(memory="the user is a nice person"),
)

# 当打开 enable_agentic_memory 时， 发现只有 qwen3:8b 才正常支持该 agent 的 tool 调用
agent_model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434")
# No session and user ID is specified, so they are generated automatically
agent = Agent(
    model=agent_model,
    memory=memory,
    # ------------ 功能 1：agent 在运行中自动决策记录什么 ------
    # 让 Agent 可以主动创建、更新或删除用户记忆。 Agent 可以在对话过程中实时决定何时更新记忆
    # Agent 可以主动决定记录什么内容， 可以包括用户问题、LLM 回复，或者任何 Agent 认为重要的信息。记录的内容由 Agent 的判断决定，更加灵活
    # 而且，它会自动开启 add_memory_references， 把记忆 加入到 下一个用户问题的 系统提示词中 
    # Agent 会根据对话内容主动决定是否删除过时或错误的记忆
    enable_agentic_memory=True,
    # ------------ 功能 2：agent 运行结束后进行对话记录 ---------
    # Agent 会在每次 run() 或 arun() 方法执行完成后，即每进行一次对话，会调用 LLM 生成 用户记忆 存储一次 记录
    # 而且，它会自动开启 add_memory_references， 把记忆 加入到 下一个用户问题的 系统提示词中 
    # 存储在 memories 字段中
    # 它记录的：从用户消息中提取和创建用户记忆，包括用户的姓名、偏好、位置信息、兴趣爱好 等重要信息
    # 当启用 enable_user_memories 时，系统使用 MemoryManager 来分析用户消息并提取记忆， MemoryManager 会配置一个 LLM 模型来执行提取任务
    enable_user_memories=True,
    # ------------  功能 3：在系统提示词中加入历史消息总结  <summary_of_previous_interactions>  给 llm 做上下文 
    # 系统会在每一个用户问题后， 都尝试本会话 所有历史消息 重新进行一次 总结
    # 而且，它会开启 add_session_summary_references ， 自动把总结 加入到 下一个用户问题的 系统提示词中 
    # 因此，本功能 有点和  add_history_to_messages 功能类似
    # 数据存储在 summaries 字段
    enable_session_summaries=True,
    #------------- 功能 4：在系统提示词中 具体历史消息记录 <memories_from_previous_interactions> 给 llm 做上下文  ----
    # 将 完整的历史对话（问题和回复） 添加到发送给模型的消息中
    add_history_to_messages=True,
    # 把最近 多少词的 消息 添加到 系统提示词中
    num_history_runs=3,
    #-------------- 功能 5： 给 llm 提供 tool 进行 消息搜索
    # Give the agent a tool to access chat history
    read_chat_history=True,
    # Add datetime to the instructions
    add_datetime_to_instructions=True,
    # -------------------------
    # 可选，没有设置这个，memory 也能工作
    # Agent 的 storage 用于存储会话状态和对话历史 （ Memory 的 storage 用于存储用户记忆和会话摘要 ）
    # 当 Agent 启动时，会通过 load_session() 方法从存储中加载现有会话
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    # storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/memory.db"),
    #-------------------------
    # debug
    debug_mode=True,
    show_tool_calls=True,
)



print("------ 第一轮 对话演示： 自动生成 session id -----")

# 每完成一次 对话，memeory 的 llm 都会对 历史的所有 消息 进行一次 summary
agent.print_response(
    "My name is John Doe .",
    stream=True,
)
agent.print_response(
    " I like to hike in the mountains on weekends.",
    stream=True,
)

memories = memory.get_user_memories()
print("--- John Doe's memories:")
pprint(memories)
session_summary = agent.get_session_summary()
pprint(session_summary)


# 跑完以后， 这次的交互中， agent 会在 系统提示词中 带入之前所有会话的 summary ， 作为背景信息
agent.print_response(
    "What are my hobbies?",
    stream=True,
)

print("------ check memory -----")
# enable_user_memories 使得
memories = memory.get_user_memories()
print("---John Doe's memories:")
pprint(memories)
session_summary = agent.get_session_summary()
pprint(session_summary)

# 查看 Memory 的完整数据字典  
memory_dict = memory.to_dict()  
pprint(memory_dict)  



print("------ 第二轮 对话演示：用一组新的 session id 来进行 memory 记录和管理 -----")

# 基于新的 session id 来进行 memory 记录和管理（ 如果以前的对话 也基于这个 id， 就会在之前的记录中 基于添加 ）
session_id_2 = "1002"
mark_gonzales_id = "mark@example.com"

agent.print_response(
    "My name is Mark Gonzales and I like anime and video games.",
    stream=True,
    user_id=mark_gonzales_id,
    session_id=session_id_2,
)

agent.print_response(
    "What are my hobbies?",
    stream=True,
    user_id=mark_gonzales_id,
    session_id=session_id_2,
)

# 使用 id 获取指定 会话的 记录
memories = memory.get_user_memories(user_id=mark_gonzales_id)
print("Mark Gonzales's memories:")
pprint(memories)

# We can get the session summary from memory as well
session_summary = memory.get_session_summary(
    session_id=session_id_2, user_id=mark_gonzales_id
)
pprint(session_summary)
