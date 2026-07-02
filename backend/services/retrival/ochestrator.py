from services.Ingestion.store_vectors import VectorDatabase
from services.Embedding.generate_embedding import GenerateEmbeddings
from backend.services.retrival.llm_generation import LLMService

from typing import AsyncGenerator


class RetrivalOchestrator:
    def __init__(
        self,
        convert_vector: GenerateEmbeddings,
        search_vector: VectorDatabase,
        llm_service: LLMService,
    ):
        self.convert_vector = convert_vector
        self.search_vector = search_vector
        self.llm_service = llm_service

    async def run(self, user_query) -> AsyncGenerator[str, None]:
        prompt_embedding = await self.convert_vector.query_to_vector(user_query)

        context_docs = await self.search_vector.search_vectors(prompt_embedding)
        context_text = "\n".join(
            [f"Source: {d['source']} Page: {d.get('page_number')}\n{d['content']}" for d in context_docs]
        )

        full_prompt = f"{context_text}\n\n{user_query}"

        async for token in self.llm_service.groq_stream_generator(full_prompt):
            yield token
