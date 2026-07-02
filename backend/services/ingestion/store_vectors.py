from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgre.crud import create_vector_record, search_vector_records


class VectorDatabase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_vector(self, doc: dict, embedding: Any):
        await create_vector_record(
            self.db,
            embedding=embedding,
            source=doc.get("filename", "unknown"),
            content=doc.get("content", ""),
            page_number=doc.get("meta_data", {}).get("page_number"),
            metadata=doc.get("meta_data", {}),
        )

    async def search_vectors(self, vectors: Any, limit: int = 5) -> list[dict]:
        records = await search_vector_records(self.db, vectors, limit=limit)
        return [
            {
                "source": record.source,
                "content": record.content,
                "page_number": record.page_number,
                "metadata": record.metadata,
            }
            for record in records
        ]
