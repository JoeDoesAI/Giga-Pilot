from __future__ import annotations

from typing import Optional
from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgre.engine import Base


class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    timestamp: Mapped[Optional[str]] = mapped_column(DateTime, index=True)
    original_name: Mapped[str] = mapped_column(String, index=True)
    stored_name: Mapped[str] = mapped_column(String, index=True, unique=True)

    user: Mapped["User"] = relationship("User", back_populates="files")
