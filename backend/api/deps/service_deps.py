# from typing import Annotated
from fastapi import Depends

from services.file_service.file_uploader import FileUploader
from api.deps.db_deps import get_db
from api.deps.uploader_deps import get_supabase


from services.file_service.file_parser import FileParser
from services.embedding_service.embedding import EmbeddingService
from services.ingestion_service.store_vectors import VectorDB
from services.qa.llm_generation import LLMService
from services.embedding_service.generate_embedding import GenerateEmbeddings

from services.ingestion_service.ochestrator import IngestionOchestrator
from services.qa.ochestrator import RetrivalOchestrator

# SupabaseDep = Annotated[AsyncClient, Depends(get_supabase)]

async def get_uploader(db = Depends(get_db),supabase=Depends(get_supabase)) -> FileUploader:
    return FileUploader(db,supabase)


async def get_ingestion(
    supabase_client = Depends(get_supabase),
    db = Depends(get_db)
) -> IngestionOchestrator:
    
   
    parser = FileParser(supabase_client=supabase_client, db=db)
    embedder = EmbeddingService()
    vector_store = VectorDB(qdrant)
    
    return IngestionOchestrator(parser, embedder, vector_store)


async def get_query_ans(qdrant=Depends(get_qdrant)) -> RetrivalOchestrator:
    
    vector_store = VectorDB(qdrant)
    embedding = GenerateEmbeddings()
    llm_service = LLMService()

    return RetrivalOchestrator(vector_store, embedding, llm_service)