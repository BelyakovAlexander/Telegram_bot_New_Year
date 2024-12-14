import datetime

from sqlalchemy import String, DateTime, func, Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Root class for all classes"""
    pass


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(40), nullable=False)
    registration_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    # attribute with default value
    last_visit: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.datetime.utcnow())
    message_to_future: Mapped[str] = mapped_column(String(200), server_default=None, nullable=True)

