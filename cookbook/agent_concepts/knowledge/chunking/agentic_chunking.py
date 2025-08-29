from agno.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder

from agno.debug import enable_debug_mode  
enable_debug_mode()

db_url = "postgresql+psycopg://ai:ai@10.20.1.60:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes_agentic1_chunking",
        db_url=db_url,
        embedder=OllamaEmbedder(id="nomic-embed-text:latest", dimensions=768 , host="http://10.20.1.60:11434" ),
    ),
    chunking_strategy=AgenticChunking(
        model=Ollama(id="qwen3:8b", host="http://10.20.1.60:11434"),
    ),
)

knowledge_base.load(recreate=True)  # Comment out after first run

agent = Agent(
    model=Ollama(id="qwen3:8b", host="http://10.20.1.60:11434"),
    knowledge=knowledge_base,
    search_knowledge=True,
    debug_mode=True,
    show_tool_calls=True,
)

agent.print_response("How to make Thai curry?", markdown=True)
