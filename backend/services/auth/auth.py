from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgre import crud as database_crud

ACCESS_TOKEN_EXPIRE_MINUTES = 3600


async def authenticate_user(
    database: AsyncSession, email: str, password: str
) -> Optional[object]:
    return await database_crud.authenticate_user(database, email, password)


async def create_user(
    database: AsyncSession,
    firstname: str,
    lastname: str,
    email: str,
    hashed_password: str,
    role: str = "user",
):
    return await database_crud.create_user(
        database, firstname, lastname, email, hashed_password, role=role
    )
