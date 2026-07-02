from typing import Any, Optional

from sqlalchemy import Integer, String, JSON
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from database.postgre.engine import Base


class DocumentChnk(Base):
    """Retrieval-ready passage with embedding for semantic search"""

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_id: Mapped[Optional[str]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True
    )
    chunk_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    embedding: Mapped[Any] = mapped_column(
        Vector(1536)
    )  # Adjust vector dimension to your embedding model
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
