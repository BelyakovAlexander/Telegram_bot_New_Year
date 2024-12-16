import asyncio
import types
import datetime

import aiogram
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from config_data.config import private_commands
from database import User
from database.engine import create_db, drop_db, get_all_users
from loader import dp, bot
from handlers import *


async def main():
    """Create database"""
    # await drop_db()                   # dropping - for TESTING purposes only
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)

    '''
    except aiogram.exceptions.TelegramBadRequest as e:
        if "chat not found" in str(e):
            logging.warning(f"Chat not found for user {user.id}, skipping...")
        else:
            raise
    '''

    async def save_send_message(bot: bot, user: User):
        try:
            await bot.send_message(chat_id=user.telegram_id, text=f'Your message to future: {user.message_to_future}')
        except aiogram.exceptions.TelegramBadRequest as e:
            if "chat not found" in str(e):
                pass
                # logging.warning(f"Chat not found for user {user.id}, skipping...")
            else:
                raise

    async def regularity_work(bot: bot):
        users: list[User] = await get_all_users()

        # gather
        task_list = []
        for user in users:
            if user.message_to_future:
                task_list.append(save_send_message(bot, user))
        await asyncio.gather(*task_list)

    execution_time = datetime.datetime(year=2024, month=12, day=16, hour=23, minute=38)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(regularity_work, trigger = 'interval', seconds = 3600, args=(bot,))
    # scheduler.add_job(regularity_work, trigger='cron', hour=12, minute=0)
    scheduler.add_job(regularity_work, trigger = DateTrigger(run_date=execution_time), args=(bot,))
    scheduler.start()

    # Задаём команды, вызываемые в боте по кнопке внизу. Список команд (объектов BotCommand) - в файле config
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
