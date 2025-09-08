from agno.agent import Agent  
from agno.storage.sqlite import SqliteStorage  
from agno.workflow.v2.step import Step  
from agno.workflow.v2.workflow import Workflow  
from agno.models.ollama import Ollama
  
from agno.workflow.v2.types import StepInput, StepOutput  
import json  
  
def print_all_step_data(step_input: StepInput) -> StepOutput:  
    """使用 JSON dump 打印所有 StepInput 数据"""  
    print("\n" + "=" * 50)  
    print("🔍 STEP INPUT JSON 数据")  
    print("=" * 50)  
      
    # 使用 StepInput 的 to_dict() 方法转换为字典，然后 JSON 序列化  
    step_data = step_input.to_dict()  
    print(json.dumps(step_data, indent=2, ensure_ascii=False, default=str))  
      
    print("=" * 50)  
    return StepOutput(  
        content="StepInput 数据已通过 JSON 打印完成",  
        success=True  
    )

# 定义三个智能体 - 移除所有工具，只做简单推理  
research_agent = Agent(  
    name="Research Agent",  
    model=Ollama(id="qwen2.5:7b",host="http://10.20.1.60:11434"),
    instructions=[  
        "基于你的知识对主题进行简单分析",  
        "只输出 3 个关键要点",  
        "每个要点一句话",  
    ],  
    show_tool_calls=True,
)  
  
analysis_agent = Agent(  
    name="Analysis Agent",   
    model=Ollama(id="deepseek-v2:16b",host="http://10.20.1.60:11434"), 
    instructions=[  
        "分析前一步的要点",  
        "只输出 2 个核心见解",  
        "每个见解一句话",  
        "保持极简"  
    ],  
    show_tool_calls=True,
)  

writer_agent = Agent(  
    name="Writer Agent",  
    model=Ollama(id="qwen3:14b",host="http://10.20.1.60:11434"),
    instructions=[  
        "基于分析写一个 50 字以内的总结",  
        "只包含最核心的结论",  
        "格式简洁"  
    ],  
    show_tool_calls=True,
)  
  
# 定义三个步骤  
research_step = Step(  
    name="Research Step",  
    agent=research_agent,  
)  
  
analysis_step = Step(  
    name="Analysis Step",   
    agent=analysis_agent,  
)  
  
writing_step = Step(  
    name="Writing Step",  
    agent=writer_agent,  
)  

data_print_step = Step(  
    name="Data Print Step",  
    executor=print_all_step_data,  
)

# 创建工作流  
if __name__ == "__main__":  
    simple_workflow = Workflow(  
        name="Ultra Simple Workflow",  
        description="极简三步骤：推理 → 分析 → 总结",  
        storage=SqliteStorage(  
            table_name="workflow_v2",  
            db_file="tmp/workflow_v2.db",   
            mode="workflow_v2",  
        ),  
        steps=[research_step, analysis_step, writing_step, data_print_step],  
        debug_mode=True,
    )  
      
    # 执行工作流 - 启用流式输出观察日志  
    simple_workflow.print_response(  
        message="AI agent frameworks 2025",  
        markdown=True,  
        stream=True,  
        stream_intermediate_steps=True,  
    )

