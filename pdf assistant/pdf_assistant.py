import os
from dotenv import load_dotenv
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import typer
from typing import Optional, List
from phi.assistant import Assistant

# Load environment variables
load_dotenv()

# Set environment variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Database URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(collection="recipes", db_url=db_url)
)

# Load knowledge base
knowledge_base.load()

def pdf_assistant(new: bool=False, user: str="user"):
    from phi.storage.assistant.postgres import PgAssistantStorage
    run_id: Optional[str] = None

    storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        run_id=run_id,
        show_tools_calls=True,
        read_chat_history=True,
    )

    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    typer.run(pdf_assistant)