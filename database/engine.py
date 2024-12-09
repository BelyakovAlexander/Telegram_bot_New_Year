import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select, update, delete
from typing import Optional
from .user_base import Base, User

engine = create_async_engine(os.getenv('USERS_DB'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    """Function  for CREATION of database tables (from 'Base'-inherited classes in user_base.py)"""
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()             # if 2 lines above was 'engine.begin()', this line shouldn't be created, but I created it for better traceability


async def drop_db():
    """Function  for DROPPING of database table"""
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()             # if 2 lines above was 'engine.begin()', this line shouldn't be created, but I created it for better traceability


async def user_registration(from_user) -> None:
    """Function for adding user in database after /start command"""
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.telegram_id == from_user.id))

        if not user:
            session.add(User(
                telegram_id=from_user.id,
                fullname=from_user.full_name
            ))
            await session.commit()


# async def save_request(user_tg_id: int, query_url: str, text: str) -> None:
#     """Save user's request to database.
#     Autocheck if requests list increase 10 lines. In this case the latest requests to be deleted"""
#     async with session_maker() as session:
#         stmnt = select(RequestsHistory.request_time, RequestsHistory.query_text).\
#                 where(RequestsHistory.user_tg_id == user_tg_id)
#         result = await session.execute(stmnt)
#         query_list = result.all()
#
#         # Deleting all latest requests in case it's quantity bigger than 10
#         while len(query_list) >= 10:
#             latest_query_stmnt = delete(RequestsHistory).\
#                                 where(RequestsHistory.query_text == query_list[0][1])
#             await session.execute(latest_query_stmnt)
#             await session.commit()
#             result = await session.execute(stmnt)
#             query_list = result.all()
#
#         session.add(RequestsHistory(user_tg_id=user_tg_id, url=query_url, query_text = text))
#         await session.commit()


async def set_future_message(from_user, new_message) -> None:
    """Function for changing of 'future_message' column in 'users' table in DB for current user"""
    async with session_maker() as session:
        stmnt = update(User).\
                where(User.telegram_id == from_user.id).\
                values(message_to_future = new_message)
        await session.execute(stmnt)
        await session.commit()


async def get_future_message(user_tg_id) -> Optional[str]:
    """Function that returns user's 'message_to_future' column data"""
    async with session_maker() as session:
        stmnt = select(User.message_to_future).\
                where(User.telegram_id == user_tg_id)
        result = await session.execute(stmnt)
        future_message: Optional[str] = result.scalars().one()
        if future_message:                                                          # TEST
            return future_message
        else:
            return None

# async def get_history(from_user):
#     """Function that returns user's history"""
#     async with session_maker() as session:
#         stmnt = select(RequestsHistory.query_text, RequestsHistory.request_time, RequestsHistory.url).\
#                 where(RequestsHistory.user_tg_id == from_user.id)
#         result = await session.execute(stmnt)
#         history = result.all()
#         return history
