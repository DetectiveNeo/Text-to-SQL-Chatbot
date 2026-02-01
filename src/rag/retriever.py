from src.rag.vector_store import VectorStore
from src.rag.create_embedding import embed_text
from src.config import Config

cfg = Config()
store = VectorStore.load(cfg.vectore_store_path)

def get_schema_context(user_prompt, k=3):
    user_prompt_embedding = embed_text(user_prompt)

    (_, relevant_schema) = store.search(user_prompt_embedding, k)

    schema_context = "\n\n".join(relevant_schema)

    return schema_context