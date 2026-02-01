"""

Raw Structure that needs to be embedded

Table: orders
Columns:
- order_id (INTEGER)
- customer_id (INTEGER)
- order_date (DATE)
- total_amount (FLOAT)

"""

import json
from openai import OpenAI
from src.config import Config
from src.rag.vector_store import VectorStore

cfg = Config()

def table_schema_to_text(table: dict) -> str:
    """
    Docstring for table_schema_to_text

    Convert one table schema dict into embedding-friendly text
    
    :param table: Description
    :type table: dict
    :return: Description
    :rtype: str
    """

    lines = [f"Table: {table['table']} "]

    if table.get("description"):
        lines.append(f"Description: {table['description']}")

    lines.append("Columns:")
    for col in table["columns"]:
        line = f"- {col['name']} ({col['type']})"
        if col.get("desc"):
            line += f": {col['desc']}"
        lines.append(line)

    return "\n".join(lines)

def embed_text(texts: list[str]) -> list[list[float]]:
    """
    Docstring for embed_text
    Function to create embeddings for the table dictionery
    
    :param texts: Description
    :type texts: list[str]
    :return: Description
    :rtype: list[list[float]]
    """
    client = OpenAI(api_key= cfg.api_key)
    
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = texts
    )

    return [item.embedding for item in response.data]

if __name__ == "__main__":

    with open(cfg.schema_path, "r") as file:
        table_schemas_json = json.load(file)

    # print(type(table_schemas_json))
    # print(table_schemas_json)

    # sample_table_text = table_schema_to_text(table_schemas_json[0])

    # print(sample_table_text)

    # sample_embedded_text = embed_text(sample_table_text)

    # print(f"Embedding Data type : {type(sample_embedded_text)}")
    # print(f"Number of Chunks: {len(sample_embedded_text)}")

    # print(f"Embedding Dimension: {len(sample_embedded_text[0])}")

    print("--------------------------------------------------------------------------")
 
    all_metadata = [table_schema_to_text(table_schema) for table_schema in table_schemas_json]

    print(type(all_metadata))
    print(len(all_metadata))
    print(all_metadata)

    embeddings = embed_text(texts= all_metadata)

    print(len(embeddings))
    print(len(embeddings[0]))

    print("Embeddings created successfully")

    store = VectorStore(dim= len(embeddings[0]))

    store.add(embeddings, all_metadata)

    store.save(path= cfg.vectore_store_path)

    print("Embeddings and meta data is stored in vector store.")










