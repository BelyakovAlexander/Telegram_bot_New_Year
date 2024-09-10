from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data import config

# create dispatcher instance for main requests filtering
dp = Dispatcher()

# create routers instances
user_router = Router()
common_router = Router()

# create bot instance
bot = Bot(token=config.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # parse mode as HTML for ALL bot's handlers
          )

# connect created router to main dispatcher
dp.include_router(user_router)

# this router has to be the last one!
dp.include_router(common_router)

