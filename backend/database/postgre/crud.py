from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import verify_password
from models.postgre.user import User
from models.postgre.file import File
from models.postgre.vector import DocumentChnk


async def get_user_by_email(database: AsyncSession, email: str) -> Optional[User]:
    result = await database.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    database: AsyncSession,
    firstname: str,
    lastname: str,
    email: str,
    hashed_password: str,
    role: str = "user",
) -> User:
    new_user = User(
        first_name=firstname,
        last_name=lastname,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )

    database.add(new_user)
    await database.commit()
    await database.refresh(new_user)

    return new_user


async def authenticate_user(
    database: AsyncSession, email: str, password: str
) -> Optional[User]:
    user = await get_user_by_email(database, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def create_file_record(
    database: AsyncSession,
    original_name: str,
    stored_name: str,
    user_id: Optional[int] = None,
) -> File:
    new_file = File(
        original_name=original_name,
        stored_name=stored_name,
    )
    if user_id:
        new_file.user_id = user_id

    database.add(new_file)
    await database.commit()
    await database.refresh(new_file)

    return new_file


async def get_original_filename_by_stored_name(
    database: AsyncSession, stored_name: str
) -> Optional[str]:
    stmt = select(File.original_name).where(File.stored_name == stored_name)
    result = await database.execute(stmt)
    return result.scalar_one_or_none()


async def create_vector_record(
    database: AsyncSession,
    embedding,
    source: str,
    content: str,
    page_number: Optional[int] = None,
    metadata: Optional[dict] = None,
    document_id: Optional[str] = None,
    chunk_id: Optional[str] = None,
) -> DocumentChunk:
    new_record = DocumentChnk(
        document_id=document_id,
        chunk_id=chunk_id,
        embedding=embedding,
        source=source,
        page_number=page_number,
        metadata=metadata,
    )

    database.add(new_record)
    await database.commit()
    await database.refresh(new_record)

    return new_record


async def search_vector_records(
    database: AsyncSession, query_embedding, limit: int = 5
) -> list[DocumentChunk]:
    stmt = (
        select(DocumentChnk)
        .order_by(DocumentChnk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    result = await database.execute(stmt)
    return result.scalars().all()
