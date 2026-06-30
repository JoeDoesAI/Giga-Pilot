from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from db.postgre.engine import engine


# Create a session maker for AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_= AsyncSession, 
    expire_on_commit=False, # Disable expire on commit for async operations
    autoflush=False
)