from aiogram import types, F

from config_data.config import DEFAULT_COMMANDS
from aiogram.filters.command import Command, CommandStart
from database.engine import user_registration
from aiogram.fsm.context import FSMContext

from keyboards import *
from loader import user_router


@user_router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext) -> None:
    await user_registration(message.from_user)
    await message.answer(f"Hello, {message.from_user.full_name}! I will help you to find a <b>good movie</b>!")
    await state.clear()


@user_router.message(F.text.lower() == 'help')
@user_router.message(Command('help'))
async def bot_help(message: types.Message, state: FSMContext) -> None:
    """Handler that activates when user's message contains 'help' OR after command '/help'"""

    text = [f"/{command} - {descr}" for command, descr in DEFAULT_COMMANDS]
    await message.answer("\n".join(text))
    await state.clear()


@user_router.message(F.text.lower() == 'menu')
@user_router.message(Command('menu'))
async def bot_help(message: types.Message, state: FSMContext) -> None:
    """Handler that activates when user's message contains 'menu' OR after command '/menu'"""

    await user_registration(message.from_user)                      # Just in case, check if user has registered
    await message.answer('Please choose any option:',
                         reply_markup=initial_kbd)
    await state.clear()


