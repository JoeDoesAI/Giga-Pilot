from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.postgre.engine import Base


class RequestLog(Base):
    __tablename__ = "request_log"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String, index=True)
    time: Mapped[str] = mapped_column(String, index=True)
    method: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String, index=True)
    status_code: Mapped[str] = mapped_column(String, index=True)
    client_ip: Mapped[str] = mapped_column(String, index=True)
