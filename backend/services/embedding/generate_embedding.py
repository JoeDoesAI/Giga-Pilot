from typing import List
from core.config import Settings
from sentence_transformers import SentenceTransformer


class GenerateEmbeddings:
    def __init__(self, 
                model:str = Settings.EMBEDDING_MODEL):
        self.encoder = SentenceTransformer(model)
        

        
    async def query_to_vector(self, query:str) -> List[str]:
        embeddings = self.encoder.encode(query)

        return embeddings