from aiogram import types, F
from aiogram.filters import StateFilter

from config_data.config import DEFAULT_COMMANDS
from aiogram.filters.command import Command, CommandStart
from database.engine import user_registration
from aiogram.fsm.context import FSMContext

from keyboards import *
from loader import user_router


@user_router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext) -> None:
    await user_registration(message.from_user)
    await message.answer(f"<b>Здравствуй, {message.from_user.full_name}</b>!\n Ждёшь чудо на Новый год? Я хочу"
                         f" поднять тебе настроение! Хочешь, погадаю?\n"
                         f"Или потренируешься быть Дедом Морозом? Тогда \n"
                         f"просто выбери эти варианты из списка внизу!",
                         reply_markup=initial_keyboard_inline)
    await state.clear()


# handler для отмены всех статусов и возвращения к началу разговора
@user_router.message(StateFilter('*'), F.text.lower() == 'отмена')
@user_router.message(Command('отмена', 'cancel'))
async def cancel_states(message: types.Message, state: FSMContext) -> None:
    await message.answer('Всё отменяем. Возвращаемся на старт!', reply_markup=initial_keyboard_inline)
    await state.clear()

# handler от ИНЛАЙН кнопки для отмены всех статусов и возвращения к началу разговора
@user_router.callback_query(StateFilter('*'), F.data == 'cancel')
async def cancel_states_inline(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Всё отменяем. Возвращаемся на старт!', reply_markup=initial_keyboard_inline)
    await state.clear()


@user_router.message(F.text.lower() == 'help')
@user_router.message(Command('help'))
async def bot_help(message: types.Message, state: FSMContext) -> None:
    """Handler that activates when user's message contains 'help' OR after command '/help'"""

    text = [f"/{command} - {descr}" for command, descr in DEFAULT_COMMANDS]
    await message.answer("\n".join(text))
    await state.clear()
