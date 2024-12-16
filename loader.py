from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data import config

# create dispatcher instance for main requests filtering
from middlewares.message_control import MessageController

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

# this router has to be connected last!
dp.include_router(common_router)

# register middleware in dispatcher (in this case - for delay before each message to avoid DDoS)
dp.message.middleware.register(MessageController())
dp.callback_query.middleware.register(MessageController())

