"""

uv venv
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
uv pip install "numpy<2" agno ollama lancedb tantivy infinity-client pylance

运行 infinity
运行 ollama

"""

from agno.agent import Agent
from agno.knowledge.url import UrlKnowledge
from agno.models.ollama import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.ollama import OllamaEmbedder
from agno.embedder.jina import JinaEmbedder
from agno.reranker.infinity import InfinityReranker

# Create a knowledge base, loaded with documents from a URL
knowledge_base = UrlKnowledge(
    # urls=["https://docs.agno.com/introduction/agents.md"],
    urls=[
        "https://docs.agno.com/introduction/agents.md",
        "https://docs.agno.com/agents/tools.md",
        "https://docs.agno.com/agents/knowledge.md",
    ],
    # Use LanceDB as the vector database, store embeddings in the `agno_docs` table
    # LanceDB 把数据写到本地磁盘中
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        # SearchType 是一个枚举类，定义了三种搜索类型：
        # - SearchType.vector - 纯向量搜索。使用嵌入向量进行语义相似性搜索
        # - SearchType.keyword - 关键词搜索， 基于传统的全文搜索，通过关键词匹配来查找文档
        # - SearchType.hybrid - 混合搜索。 结合向量搜索和关键词搜索的优势，既能找到语义相似的内容，也能精确匹配关键词
        search_type=SearchType.hybrid,
        # 使用 本地部署的 ollama 实施 embedding
        #embedder=OllamaEmbedder(id="nomic-embed-text:latest", dimensions=768 , host="http://10.20.1.60:11434" ),
        # 使用 Infinity 做 embedding
        embedder=JinaEmbedder(
            id="jinaai/jina-embeddings-v3",
            base_url="http://10.20.1.60:7997/embeddings",  # 指向您的 Infinity 服务
            api_key="dummy_key",  # Infinity 不需要，可使用虚拟 key 绕过验证  
            dimensions=1024
        ),
        # 使用本地部署的 Infinity 做 reranker
        # 注意：agno 没有 reranking 的日志，reranking 是向量数据库来实施的。我们可以在 infinity 服务的日志中查看调用日志
        # https://michaelfeil.eu/infinity/main/deploy/
        reranker=InfinityReranker(
            model="BAAI/bge-reranker-base",  # You can change this to other models
            host="10.20.1.60",
            port=7997,
            top_n=5,  # Return top 5 reranked documents
        ),
    ),
)

agent = Agent(
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
    knowledge=knowledge_base,
    # search_knowledge=True gives the Agent the ability to search on demand
    # search_knowledge is True by default
    search_knowledge=True,
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Include sources in your response.",
        "Always search your knowledge before answering the question.",
        "Provide detailed and accurate information based on the retrieved documents.",
    ],
    markdown=True,
    debug_mode=True  # 开启调试模式  ， 包含了详细的 llm 指标、消息交互、工具调用过程
)

if __name__ == "__main__":
    # Load the knowledge base, comment after first run
    knowledge_base.load(recreate=True)
    agent.print_response(
         "What is the difference between knowledge and tools?",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )
