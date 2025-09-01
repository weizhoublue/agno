"""

浏览器访问 http://localhost:8001/docs ，  可以了解 API 文档和可用的 url 

访问服务

curl -X POST "http://localhost:8001/runs?agent_id=basic_agent" \
  -d "message=Hello, how are you?" | jq .


curl -X POST "http://localhost:8001/runs?agent_id=basic_agent" \
  -d "message=Hello, how are you?" \
  -d "stream=false" \
  -d "session_id=my_session_123" \
  -d "user_id=user_456"   | jq .


确认状态
curl -X GET "http://localhost:8001/status"


"""

from agno.agent import Agent
from agno.app.fastapi import FastAPIApp
from agno.models.ollama import Ollama

basic_agent = Agent(
    name="Basic Agent",
    # 这个 id 觉得了 外部访问的 http url
    agent_id="basic_agent",
    model=Ollama(id="qwen3:8b",host="http://10.20.1.60:11434"),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True,
)

fastapi_app = FastAPIApp(
    agents=[basic_agent],
    name="Basic Agent",
    # 这个 id 不影响外部访问的 http url，
    app_id="basic3_agent",
    description="A basic agent that can answer questions and help with tasks.",
)

app = fastapi_app.get_app()
if __name__ == "__main__":
    fastapi_app.serve(
        # 是一个模块路径字符串，告诉 uvicorn 从哪里导入 FastAPI 应用实例
        # 从 basic.py 中的变量 app 导入
        app="basic:app", 
        port=8001, 
        # 当本 py 代码改变，自动重新加载
        reload=True,
    )




