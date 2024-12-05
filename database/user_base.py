import datetime

from sqlalchemy import String, DateTime, func, Integer, BigInteger, ForeignKey
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
    message_to_future: Mapped[str] = mapped_column(String(200), nullable=True)


# class RequestsHistory(Base):
#     __tablename__ = 'requests_history'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     url: Mapped[str] = mapped_column(String(300))
#     query_text: Mapped[str] = mapped_column(String(30))
#     user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
#     # user_name: Mapped[str] = mapped_column(ForeignKey('users.fullname'))
#     request_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

# class Movie(Base):
#     __tablename__ = 'movies'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     rating: Mapped[str] = mapped_column(String(10)) # string (not float) for our convenience
#     name: Mapped[str] = mapped_column(String(90), nullable=False)
#     description: Mapped[str] = mapped_column(String(250))
#     genre: Mapped[str] = mapped_column(String(40))
#     country: Mapped[str] = mapped_column(String(40))
#     year: Mapped[int] = mapped_column(Integer)
