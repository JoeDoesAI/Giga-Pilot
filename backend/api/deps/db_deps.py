from typing import AsyncGenerator
from db.postgre.session import AsyncSession, AsyncSessionLocal
# from qdrant_client import AsyncQdrantClient
# from fastapi import Request

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session

    finally:
        await session.close()

# async def get_qdrant(request:Request) -> AsyncQdrantClient:
#     return  request.app.state.qdrant

