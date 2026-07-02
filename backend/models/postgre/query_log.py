from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.postgre.engine import Base


class QueryLog(Base):
    __tablename__ = "query_log"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String, index=True)
    time: Mapped[str] = mapped_column(String, index=True)
    query_text: Mapped[str] = mapped_column(String, index=True)
    query_length: Mapped[int] = mapped_column(Integer, index=True)
    response: Mapped[str] = mapped_column(String, index=True)
    response_length: Mapped[str] = mapped_column(String, index=True)
