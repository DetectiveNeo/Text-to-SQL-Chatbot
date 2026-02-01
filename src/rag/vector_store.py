import faiss
import numpy as np
import pickle

from src.config import Config

class VectorStore:
    def __init__(self, dim : int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadata):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

        # assert len(self.index) == len(self.metadata) , "Number of embeddings are not equal to the number of meta data of tables"

    def search(self, query_embedding, k= 3):
        query = np.asarray([query_embedding]).astype("float32")
        # Returen the top k vector store embedding indices which matches with the query
        # indices = [[4, 0, 7]]
        # distances = [[0.12, 0.45, 0.88]]
        distances, indices = self.index.search(query, k)
        return distances[0], [self.metadata[i] for i in indices[0]]
    
    def save(self, path):
        faiss.write_index(self.index, str(path.with_suffix(".index")))
        with open(path.with_suffix(".meta"), "wb") as file:
            pickle.dump(self.metadata, file)

    @classmethod
    def load(cls, path):
        index = faiss.read_index(str(path.with_suffix(".index")))
        with open(path.with_suffix(".meta"), "rb") as file:
            metadata = pickle.load(file)
        
        store = cls(index.d)
        store.index = index
        store.metadata = metadata

        return store
    

if __name__ == "__main__":

    cfg = Config()

    # # 2D embeddings so we can reason easily
    # embeddings = [
    #     [1.0, 1.0],   # point A
    #     [2.0, 2.0],   # point B
    #     [10.0, 10.0], # point C
    # ]

    # metadata = [
    #     "Employee table",
    #     "Department table",
    #     "Sales table",
    # ]

    # store = VectorStore(dim= len(embeddings[0]))
    # store.add(embeddings, metadata)

    # query_embedding = [1.5,1.5]

    # distances, results = store.search(query_embedding, k= 2)

    # print(f"Distance: {distances}")
    # print(f"Results: {results}")

    # store.save(path= cfg.vectore_store_path)

    new_store = VectorStore.load(path= cfg.vectore_store_path)

    (distances , results) = new_store.search(query_embedding= [1.5,1.5], k= 2)
    print(f"Distance: {distances}")
    print(f"Results: {results}")






    






