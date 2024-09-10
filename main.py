import asyncio
import types

from config_data.config import private_commands
from loader import dp, bot
from handlers import *


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    # Задаём команды, вызываемые в боте по кнопке внизу. Список команд (объектов BotCommand) - в файле config
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())