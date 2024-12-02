import os
from aiogram.types import BotCommand
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Commands list issued after "/help" command (see user_handlers)
DEFAULT_COMMANDS = (
    ("start", "Bot launch (actually, it doing nothing after that...)"),
    ("help", "Show commands... Again."),
    ("menu", "Show menu"),
    ('cancel', 'Cancel any progress in search or survey')
)
# Список стандартных команд для бота, доступных по кнопке внизу
private_commands = [
    BotCommand(command='start', description="Let's START!"),
    BotCommand(command='help', description="Show all commands"),
    BotCommand(command='menu', description="Show menu with BUTTONS"),
    BotCommand(command='cancel', description='Cancel progress during search or survey')
]
