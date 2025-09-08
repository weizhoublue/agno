from agno.agent import Agent  
from agno.models.ollama import Ollama  
from agno.workflow.v2.step import Step  
from agno.workflow.v2.workflow import Workflow  
from agno.storage.sqlite import SqliteStorage  
  
# === 简单的工具函数 ===  
def add_to_state(agent: Agent, key: str, value: str) -> str:  
    """往 workflow_session_state 添加数据"""  
    if agent.workflow_session_state is None:  
        agent.workflow_session_state = {}  
      
    agent.workflow_session_state[key] = value  
    return f"✅ 已添加到状态: {key} = {value}"  
  
def read_from_state(agent: Agent, key: str) -> str:  
    """从 workflow_session_state 读取数据"""  
    if (agent.workflow_session_state is None or   
        key not in agent.workflow_session_state):  
        return f"❌ 状态中没有找到: {key}"  
      
    value = agent.workflow_session_state[key]  
    return f"📖 从状态读取: {key} = {value}"  
  
# === 创建两个 AGENT ===  
writer_agent = Agent(  
    name="Writer Agent",  
    model=Ollama(id="qwen3:14b", host="http://10.20.1.60:11434"),  
    tools=[add_to_state],  
    instructions=[  
        "你负责往共享状态写入信息",  
        "使用 add_to_state 工具添加用户要求的内容",  
        "保持简洁回复"  
    ],
    show_tool_calls=True,
)  
  
reader_agent = Agent(  
    name="Reader Agent",   
    model=Ollama(id="qwen3:14b", host="http://10.20.1.60:11434"),  
    tools=[read_from_state],  
    instructions=[  
        "你负责从共享状态读取信息",  
        "使用 read_from_state 工具读取之前存储的内容",  
        "保持简洁回复"  
    ]  ,
    show_tool_calls=True,
)  
  
# === 创建步骤 ===  
write_step = Step(  
    name="Write to State",  
    agent=writer_agent  
)  
  
read_step = Step(  
    name="Read from State",  
    agent=reader_agent  
)  
  
# === 创建工作流 ===  
if __name__ == "__main__":  
    state_workflow = Workflow(  
        name="State Share Workflow",  
        description="演示 workflow_session_state 共享",  
        steps=[write_step, read_step],  
        workflow_session_state={},  # 初始化空状态  
        storage=SqliteStorage(  
            table_name="workflow_v2",  
            db_file="tmp/workflow_v2.db",  
            mode="workflow_v2"  
        ),  
        debug_mode=True  
    ) 
      
    print("🚀 开始状态共享工作流")  
    print("=" * 50)  
      
    # 执行工作流  
    state_workflow.print_response(  
        message="请添加一个键值对 'project_name' = 'AI助手开发'，然后读取这个值",  
        markdown=True,  
        stream=True,  
        stream_intermediate_steps=True  
    )  
      
    print("\n" + "=" * 50)  
    print("🔍 最终 workflow_session_state:")  
    print("=" * 50)  
    import json  
    print(json.dumps(state_workflow.workflow_session_state, indent=2, ensure_ascii=False))
