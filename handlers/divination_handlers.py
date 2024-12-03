from aiogram import types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from keyboards import del_keyboard, initial_kbd
from loader import user_router
from states.user_states import RequestInfo
import random

divination_list = ('В новом году Вас ждет много радостных моментов и приятных сюрпризов!',
                   'Этот год принесет Вам новые знакомства и укрепит старые связи.',
                   'Ваша жизнь наполнится теплом, любовью и гармонией.',
                   'Все Ваши начинания будут успешными, а цели – достижимыми.',
                   'Вас ждет путешествие, полное незабываемых впечатлений.',
                   'В новом году Вы обретете уверенность в себе и своих силах.',
                   'Вас ожидает неожиданный подарок судьбы, который изменит Вашу жизнь к лучшему.',
                   'Год будет полон вдохновения и творческих успехов.',
                   'Ваше здоровье будет крепким, а настроение – прекрасным.',
                   'Вас ждет финансовое благополучие и стабильность.')


# handler for starting survey
@user_router.message(StateFilter(None), F.text.lower() == 'погадай')
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Итак, {message.from_user.full_name or 'дружок'}, проведём гадание!\nНапиши, пожалуйста, как тебе нравится, чтобы тебя называли?: ",
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
