# docker run -d \
#   -e POSTGRES_DB=ai \
#   -e POSTGRES_USER=ai \
#   -e POSTGRES_PASSWORD=ai \
#   -e PGDATA=/var/lib/postgresql/data/pgdata \
#   -v pgvolume:/var/lib/postgresql/data \
#   -p 5532:5432 \
#   --name pgvector \
#   agnohq/pgvector:16

from agno.agent import Agent
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder

db_url = "postgresql+psycopg://ai:ai@10.20.1.60:5532/ai"
pdf_url = "https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"

knowledge_base = PDFUrlKnowledgeBase(
    # 通过在线的 url 获取 pdf 文件
    urls=[pdf_url],
    vector_db=PgVector(
            table_name="recipes", 
            db_url=db_url,
            # nomic-embed-text:latest 的 向量维度是 768 
            # ollama show nomic-embed-text:latest | grep "embedding length"
            embedder=OllamaEmbedder(id="nomic-embed-text:latest", dimensions=768 , host="http://10.20.1.60:11434" ),
        ),
)
# 如果之前创建过向量数据库的同名 table ， embedder dimensions 和同其匹配。否则，可以设置 recreate=True 来重新创建
knowledge_base.load(recreate=True)  # Comment out after first run

agent = Agent(
    # 模型要支持 tool
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response("How to make Thai curry?", markdown=True)
