from agno.agent import Agent
from agno.models.ollama import Ollama

from agno.debug import enable_debug_mode
# 启用调试模式
enable_debug_mode()


agent = Agent(
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    ## instructions 作为 系统提示词的一部分， 会随着用户消息一起发送给 LLM
    ## 我们可以使用 state 中的变量，来替换 instructions 中的占位符
    instructions="Users name is {user_name} and age is {age}",
    # 将 state 中的变量，添加到 发送给 LLM 的消息中
    add_state_in_messages=True,
    debug_mode=True,
)

#----------- 第一个用户对话 -------------
# Sets the session state for the session with the id "user_1_session_1"
agent.print_response(
    "What is my name?",
    session_id="user_1_session_1",
    user_id="user_1",
    # 这里的 json 数据，对 instructions 中的占位符进行替换
    session_state={"user_name": "John", "age": 30},
)

print(f"Session state: {agent.session_state}")
# 在相同的用户会话下， 之前的  "Users name is John and age is 30" 会继续被加入到 系统提示词中
agent.print_response(
    "How old am I?",
    session_id="user_1_session_1",
    user_id="user_1",
    stream=True,
)

#----------- 第二个用户对话 -------------

# Sets the session state for the session with the id "user_2_session_1"
agent.print_response(
    "What is my name?",
    session_id="user_2_session_1",
    user_id="user_2",
    session_state={"user_name": "Jane", "age": 25},
)

print(f"Session state: {agent.session_state}")
# 在相同的用户会话下， 之前的  "Users name is Jane and age is 25" 会继续被加入到 系统提示词中
agent.print_response("How old am I?", session_id="user_2_session_1", user_id="user_2")

