"""
Docstring for src.llm.pipeline.py

"""

from openai import OpenAI
import json
import sqlite3
from src.config import Config
from src.rag.create_embedding import embed_text
from src.rag.vector_store import VectorStore
from src.data_ingestion.access_db import read_sql_query
from src.rag.retriever import get_schema_context
from src.llm.prompt import SYSTEM_PROMPT, build_user_prompt
from src.llm.llm import generate_sql

cfg = Config()

def nl2sql(question: str):
    # 1. RAG
    schema_context = get_schema_context(question)
    # print(schema_context)
    # 2. Prompt
    enriched_user_prompt = build_user_prompt(schema_context, question)
    # print(enriched_user_prompt)

    # 3. LLM
    llm_sql_query = generate_sql(SYSTEM_PROMPT, enriched_user_prompt)
    # print(llm_sql_query)

    # 4. Execute
    return read_sql_query(db=cfg.database_path, sql= llm_sql_query)

if __name__ == "__main__":

    user_prompt = """
        What is the total unit cost for different delivery regions in orders table?
    """

    df = nl2sql(user_prompt)

    print(df)