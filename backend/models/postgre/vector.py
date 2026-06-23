from sqlalchemy import Column, Integer,JSON,UUID
from pgvector.sqlalchemy import Vector
from db.postgre.engine import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(UUID)
    embedding = Column(Vector(3))  # Match your vector dimension
    metadata = Column(JSON)
