from typing import AsyncGenerator
from database.postgre.session import AsyncSession, AsyncSessionLocal


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session

    finally:
        await session.close()
