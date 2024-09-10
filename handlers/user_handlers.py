from aiogram import types, F

from config_data.config import DEFAULT_COMMANDS
from aiogram.filters.command import Command, CommandStart

from keyboards import *
from loader import user_router


@user_router.message(CommandStart())
async def bot_start(message: types.Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}! I will help you to find a <b>good movie</b>!")


# activates when user's message contains 'help' OR after command '/help'
@user_router.message(F.text.lower() == 'help')
@user_router.message(Command('help'))
async def bot_help(message: types.Message) -> None:
    text = [f"/{command} - {deskr}" for command, deskr in DEFAULT_COMMANDS]
    await message.answer("\n".join(text))


# see above for 'help'
@user_router.message(F.text.lower() == 'menu')
@user_router.message(Command('menu'))
async def bot_help(message: types.Message) -> None:
    await message.answer('Please choose any option:',
                         reply_markup=initial_kbd)

