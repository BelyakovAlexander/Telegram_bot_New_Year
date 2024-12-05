from aiogram import types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from keyboards import del_keyboard, initial_kbd
from loader import user_router
from states.user_states import RequestInfo
import random

divination_list = ('В новом году тебя ждет много радостных моментов и приятных сюрпризов!',
                   'Этот год принесет тебе новые знакомства и укрепит старые связи.',
                   'Твоя жизнь наполнится теплом, любовью и гармонией.',
                   'Все твои начинания будут успешными, а цели – достижимыми.',
                   'Тебя ждет путешествие, полное незабываемых впечатлений.',
                   'В новом году ты обретёшь уверенность в себе и своих силах.',
                   'Тебя ожидает неожиданный подарок судьбы, который изменит твою жизнь к лучшему.',
                   'Год будет полон вдохновения и творческих успехов.',
                   'Твоё здоровье будет крепким, а настроение – прекрасным.',
                   'Тебя ждет финансовое благополучие и стабильность.')


# handler for starting survey
@user_router.message(StateFilter(None), F.text.lower() == 'погадай')
@user_router.callback_query(F.data == 'divine')                              # TODO (с этим декоратором бот отвечает не сообщением, а всплывающим окном с тем же текстом)
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Итак, {message.from_user.full_name or 'дружок'}, проведём гадание!\nНапиши, пожалуйста, как тебе нравится, чтобы тебя называли? ",
                         reply_markup=del_keyboard)
    await state.set_state(RequestInfo.name)


@user_router.message(RequestInfo.name, F.text)
async def divination(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name = message.text)
    res = await state.get_data()
    username = res['name']
    await message.answer(username + '! ' + random.choice(divination_list), reply_markup=initial_kbd)
    await state.clear()


@user_router.message(RequestInfo.name)
async def get_name_error(message: types.Message) -> None:
    await message.answer('Извини, не могу разобрать твой ответ. Попробуй, пожалуйста, ещё разок.')


# @user_router.message(RequestInfo.surname, F.text)
# async def get_surname(message: types.Message, state: FSMContext) -> None:
#     await state.update_data(surname=message.text)
#     await message.answer('Enter your age: ')
#     await state.set_state(RequestInfo.age)
#
#
# @user_router.message(RequestInfo.surname)
# async def get_surname_error(message: types.Message) -> None:
#     await message.answer('Wrong answer type. Please, use text only.')
#
#
# @user_router.message(RequestInfo.age)
# async def get_age(message: types.Message, state: FSMContext) -> None:
#     if message.text.isdigit():
#         await state.update_data(age=message.text)
#         res = await state.get_data()
#         await message.answer(f"Well, let's summarize:\n"
#                              f"Name: {res['name']}\n"
#                              f"Surname: {res['surname']}\n"
#                              f"Age: {res['age']} years")
#         await state.clear()
#     else:
#         await message.answer(f"You try to cheat me, {message.from_user.full_name}?\n"
#                              f"Enter your real age.")
