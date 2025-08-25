# Agent Knowledge
 
### 1. Create a virtual environment

```shell
uv venv
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
uv pip install -U pgvector "psycopg[binary]" sqlalchemy openai agno pypdf bs4

 
``` 

### 3. Run PgVector

```shell
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:16
```

### 4. Test Knowledge Cookbooks

Eg: PDF URL Knowledge Base

- Run the PDF URL script

```shell
python cookbook/agent_concepts/knowledge/pdf_url.py
```
