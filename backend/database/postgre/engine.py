from core.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = Settings.DATABASE_URL

# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, 
                             echo=False, 
                             future=True, 
                             connect_args={"statement_cache_size": 0})

Base = declarative_base()
