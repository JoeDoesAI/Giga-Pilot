import asyncio
from supabase import create_async_client
from core.config import Settings
from celery_app import celery_app
from database.postgre.session import AsyncSessionLocal
from services.file.parse import FileParser
from services.embedding.embedding import EmbeddingService
from services.ingest.store_vectors import VectorDatabase
from services.ingest.ochestrator import IngestionOchestrator


@celery_app.task(name="ingest_files")
def ingest_files() -> str:
    async def run_ingestion() -> str:
        supabase_client = await create_async_client(Settings.SUPABASE_URL, Settings.SUPABASE_KEY)
        try:
            async with AsyncSessionLocal() as database:
                parser = FileParser(supabase_client=supabase_client, database=database)
                embedder = EmbeddingService()
                vector_store = VectorDatabase(database)
                orchestrator = IngestionOchestrator(parser, embedder, vector_store)
                return await orchestrator.run()
        finally:
            await supabase_client.close()

    return asyncio.run(run_ingestion())
