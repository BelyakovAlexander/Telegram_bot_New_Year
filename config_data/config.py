import os
from aiogram.types import BotCommand
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DELAY = 1.5

# Commands list issued after "/help" command (see user_handlers)
DEFAULT_COMMANDS = (
    ("start", "Начать общение!"),
    ("help", "Показать доступные команды"),
    ('cancel', 'Давай вернёмся к началу разговора')
)
# Список стандартных команд для бота, доступных по кнопке внизу. ***Названия - только латиницей!***
private_commands = [
    BotCommand(command='start', description="Начать наше общение!"),
    BotCommand(command='help', description="Какие команды знает бот?"),
    BotCommand(command='cancel', description='Давай вернёмся к началу разговора')
]
