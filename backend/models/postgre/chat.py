from __future__ import annotations

from typing import List
from datetime import datetime

from sqlalchemy import DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgre.engine import Base


# one user can have many chats
# one chat can have many messages


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    chat_name: Mapped[str] = mapped_column(String, index=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="chats")
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete"
    )


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))

    role: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    chat: Mapped[Chat] = relationship("Chat", back_populates="messages")
    citations: Mapped[List["Citation"]] = relationship(
        "Citation", back_populates="message"
    )


class Citation(Base):
    __tablename__ = "citation"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("message.id"))

    source: Mapped[str] = mapped_column(String)
    snippet: Mapped[str] = mapped_column(String)

    message: Mapped[Message] = relationship("Message", back_populates="citations")
