
from src.config import Config
from src.rag.create_embedding import embed_text
from src.rag.vector_store import VectorStore

cfg = Config()

user_prompt = """
        What is the total unit cost for different delivery regions in the sales order table ?
    """

embedded_user_prompt = embed_text(user_prompt)

print(len(embedded_user_prompt))

store = VectorStore.load(path= cfg.vectore_store_path)

(_, relevant_schema) = store.search(query_embedding= embedded_user_prompt, k= 3)

print(len(relevant_schema))
print(relevant_schema)

