import asyncio
from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
from agno.debug import enable_debug_mode

# 启用调试模式，就能看到页面爬取过程  
enable_debug_mode()

db_url = "postgresql+psycopg://ai:ai@10.20.1.60:5532/ai"

# Create a knowledge base with the seed URLs
# 爬取遵循如下原则：
#   - 爬取的链接，必须属于同一主域名 （注： 对于 https://docs.agno.com/introduction，主域名被识别为 agno.com。因此，community.agno.com 也被认为是同一主域名下的子域名 ）
#   - 排除特定文件类型（.pdf, .jpg, .png） ， 不能是已访问过的链接 
#   - 链接的具体顺序取决于它们在HTML中的出现顺序，因为 BeautifulSoup 的 find_all("a") 按文档顺序返回链接。这意味着页面中较早出现的链接会被优先添加到爬取队列中
#   - 有的网站页面，发现无法爬取， 其 html 页面结构 可能无法满足内部代码的实现逻辑，只查找特定的 HTML 标签和 CSS 类
knowledge_base = WebsiteKnowledgeBase(
    # 从以下指定的页面开始爬取 ，在页面中出现的各种链接，都会成为被爬取的对象 
    urls=["https://spidernet-io.github.io/spiderpool/v1.0/"],
    # Number of links to follow from the seed URLs   成功爬取并提取到内容的页面数量 ， 失败的访问尝试不算
    max_links=2,
    # 可选，默认 max_depth=3 。  从起始页面开始，最大支持的跳转页面的深度
    max_depth=2,
    # Table name: ai.website_documents
    vector_db=PgVector(
        table_name="website_documents",
        db_url=db_url,
        embedder=OllamaEmbedder(id="nomic-embed-text:latest", dimensions=768 , host="http://10.20.1.60:11434" ),
    ),
)

# Load the knowledge base
# 同步加载的方式， WebsiteKnowledgeBase 在爬取页面过程中无法 处理 http 重定向
# knowledge_base.load(recreate=True)

# Create an agent with the knowledge base
agent = Agent(
    model=Ollama(id="llama3.1:latest",host="http://10.20.1.60:11434"),
    knowledge=knowledge_base,
    search_knowledge=True,
    debug_mode=True,
    show_tool_calls=True,
)

 
if __name__ == "__main__":
    
    # 使用异步加载的方式， WebsiteKnowledgeBase 在爬取页面过程中就能够 处理 http 重定向
    asyncio.run(knowledge_base.aload(recreate=True))

    # Create and use the agent
    asyncio.run(agent.aprint_response("How does spiderpool work?", markdown=True))

