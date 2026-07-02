from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgre.engine import Base


class User(Base):
    """"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), index=True)
    # role: 'user' or 'admin'
    role: Mapped[str] = mapped_column(String(50), index=True, default="technician")

    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="user")
    files: Mapped[List["File"]] = relationship("File", back_populates="user")

