from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.engine import set_future_message, get_future_message
from loader import user_router
from states.user_states import QuizStates


@user_router.callback_query(StateFilter(None), F.data == 'future')
async def change_future_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Задайте сообщение на будущий Новый Год!')
    await state.set_state(QuizStates.setting_future_message)


@user_router.message(QuizStates.setting_future_message, F.text)
async def setting_future_msg(message: types.Message, state: FSMContext):
    await message.answer(f'Распознано: {message.text}')
    await set_future_message(message.from_user, new_message=message.text)
    await state.clear()                                             #TEST
