from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pgvector import PgVector
from agno.embedder.ollama import OllamaEmbedder
from pathlib import Path
from agno.models.ollama import Ollama

db_url = "postgresql+psycopg://ai:ai@10.20.1.60:5532/ai"

# Create a knowledge base with the PDFs from the data/pdfs directory
knowledge_base = PDFKnowledgeBase(
    # 通过本地文件路径获取 pdf 文件 . 
    # 可以指向包含多个PDF的目录，可以指向某个文件，或者使用 PDFUrlKnowledgeBase 的 load_document() 方法分别加载多个 pdf
    path= Path(__file__).parent.joinpath("ThaiRecipes.pdf"),
    # path="data/pdfs",
    vector_db=PgVector(
        table_name="pdf_documents",
        # Can inspect database via psql e.g. "psql -h localhost -p 5432 -U ai -d ai"
        db_url=db_url,
        embedder=OllamaEmbedder(id="nomic-embed-text:latest", dimensions=768 , host="http://10.20.1.60:11434" ),
    ),
    reader=PDFReader(chunk=True),
)
# Load the knowledge base
knowledge_base.load(recreate=True)

# Create an agent with the knowledge base
agent = Agent(
    # 模型要支持 tool
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    knowledge=knowledge_base,
    search_knowledge=True,
)

# Ask the agent about the knowledge base
agent.print_response("Ask me about something from the knowledge base", markdown=True)
