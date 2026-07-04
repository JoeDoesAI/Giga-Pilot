from fastapi import Depends

from services.file.upload import FileUploader
from api.deps.database import get_database
from api.deps.upload import get_supabase

from services.file.parse import FileParser
from services.embedding.embedding import EmbeddingService
from services.ingest.store_vectors import VectorDatabase
# from services.retrival.llm_generation import LLMService
# from services.embedding.generate_embedding import GenerateEmbeddings

from services.ingest.ochestrator import IngestionOchestrator
# from services.retrival.ochestrator import RetrivalOchestrator


async def get_uploader(
    database=Depends(get_database), supabase=Depends(get_supabase)
) -> FileUploader:
    return FileUploader(database, supabase)


async def get_ingestion(
    supabase_client=Depends(get_supabase), database=Depends(get_database)
) -> IngestionOchestrator:
    parser = FileParser(supabase_client=supabase_client, database=database)
    embedder = EmbeddingService()
    vector_store = VectorDatabase(database)

    return IngestionOchestrator(parser, embedder, vector_store)


# async def get_query_ans(database=Depends(get_database)) -> RetrivalOchestrator:
#     vector_store = VectorDatabase(database)
#     embedding = GenerateEmbeddings()
#     llm_service = LLMService()

#     return RetrivalOchestrator(embedding, vector_store, llm_service)
