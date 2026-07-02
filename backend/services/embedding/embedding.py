from typing import List
# from transformers import AutoTokenizer, AutoModel
# import torch
from google import genai
from core.config import Settings

API_KEY = Settings.EMBEDDING_API_KEY

class EmbeddingService:
    def __init__(self, model_name: str = Settings.EMBEDDING_MODEL):
        self.client = genai.Client(api_key=API_KEY)
        self.model = model_name



    def run(self, pages:List[dict]) -> List:

        tokens = self.client.models.embed_content(
            model= self.model,
            contents = pages
        )

        return tokens 
            




















        # self.model.eval()

    # def embed_text(self, text: str):
    #     tokens = self.tokenizer(
    #         text, return_tensors="pt", return_offsets_mapping=True, truncation=False
    #     )

    #     input_ids = tokens["input_ids"]
    #     offsets = tokens["offset_mapping"][0]

    #     with torch.no_grad():
    #         output = self.model(input_ids)

    #     token_embeddings = output.last_hidden_state[0]

    #     return token_embeddings, offsets

    # def split_sentences(self, text):
    #     sentences = text.split(".")
    #     chunks = []
    #     cursor = 0
    #     for s in sentences:
    #         start = cursor
    #         end = start + len(s)
    #         chunks.append((start, end))
    #         cursor = end + 1
    #     return chunks






        # for page in pages:
        #     text = page['file_content']

        # token_embeddings, offsets = self.embed_text(text)
        
        # chunks = self.split_sentences(text)
        # chunk_embeddings = []

        # for start, end in chunks:
        #     token_idxs = [
        #         i for i, (s, e) in enumerate(offsets) if s < end and e > start
        #     ]

        #     if not token_idxs:
        #         continue

        #     emb = token_embeddings[token_idxs].mean(dim=0)
        #     chunk_embeddings.append(emb)

        # if not chunk_embeddings:
        #     return []

        # vectors = [t.detach().cpu().tolist() for t in chunk_embeddings]

        # return vectors




















