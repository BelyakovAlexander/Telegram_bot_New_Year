from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.engine import set_future_message, get_future_message, user_registration
from loader import user_router
from states.user_states import QuizStates
from keyboards.user_inline_keyboards import set_or_show_future_message, initial_keyboard_inline


@user_router.callback_query(StateFilter(None), F.data == 'future')
async def choose_future_mssg_option(callback: CallbackQuery, state: FSMContext):
    await user_registration(callback.from_user)                                         # Just for sure - second registration attempt
    await callback.message.answer('Задать новое сообщение или посмотреть уже написанное ранее?',
                                  reply_markup=set_or_show_future_message)
    await state.set_state(QuizStates.go_to_setting_future_message)


@user_router.callback_query(StateFilter(QuizStates.go_to_setting_future_message), F.data == 'set_future')
async def change_future_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Задайте сообщение на будущий Новый Год!')
    await state.set_state(QuizStates.setting_future_message)


@user_router.message(QuizStates.setting_future_message, F.text)
async def setting_future_msg(message: types.Message, state: FSMContext):
    await message.answer(f'Записал', reply_markup=initial_keyboard_inline)
    await set_future_message(message.from_user, new_message=message.text)
    await state.clear()


@user_router.callback_query(StateFilter(QuizStates.go_to_setting_future_message), F.data == 'show_future_message')
async def show_user_future_message(callback: CallbackQuery, state: FSMContext):
    mssg = await get_future_message(user_tg_id=callback.from_user.id)
    if mssg:
        await callback.message.answer(f'Твоё сообщение в будущее: \n <b>{mssg}</b>')
    else:
        await callback.message.answer(f'Ты пока не написал себе сообщение в будущее.')
    await state.clear()
