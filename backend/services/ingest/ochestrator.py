import asyncio
from typing import List

from services.file.parse import FileParser
from services.embedding.embedding import EmbeddingService
from services.ingest.store_vectors import VectorDatabase


class IngestionOchestrator:
    def __init__(
        self,
        file_parser: FileParser,
        embedder: EmbeddingService,
        vector_store: VectorDatabase,
    ):
        self.parse_file = file_parser
        self.embedder = embedder
        self.vector_store = vector_store

    async def run(self) -> str:
        documents = await self.parse_file.parse_all()
        if not documents:
            return "No documents found for ingestion."

        embeddings = self.embedder.run(documents)

        for doc, embedding in zip(documents, embeddings):
            await self.vector_store.store_vector(doc, embedding)

        return "Ingestion complete!"
