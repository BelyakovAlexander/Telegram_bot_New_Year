from aiogram import types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from keyboards import del_keyboard, initial_kbd
from loader import user_router
from states.user_states import RequestInfo


# handler for canceling all states
@user_router.message(StateFilter('*'), F.text.lower() == 'cancel')
@user_router.message(Command('cancel'))
async def cancel_states(message: types.Message, state: FSMContext) -> None:
    await message.answer('Cancel all. Return to start', reply_markup=initial_kbd)
    await state.clear()


# handler for starting survey
@user_router.message(StateFilter(None), F.text.lower() == 'user info survey')
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"So, you want to start our quiz, {message.from_user.full_name}?\nEnter your name: ",
                         reply_markup=del_keyboard)
    await state.set_state(RequestInfo.name)


@user_router.message(RequestInfo.name, F.text)
async def get_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name = message.text)
    await message.answer('Enter your surname: ')
    await state.set_state(RequestInfo.surname)

@user_router.message(RequestInfo.name)
async def get_name_error(message: types.Message) -> None:
    await message.answer('Wrong answer type. Please, use text only.')


@user_router.message(RequestInfo.surname, F.text)
async def get_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    await message.answer('Enter your age: ')
    await state.set_state(RequestInfo.age)


@user_router.message(RequestInfo.surname)
async def get_surname_error(message: types.Message) -> None:
    await message.answer('Wrong answer type. Please, use text only.')


@user_router.message(RequestInfo.age)
async def get_age(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(age=message.text)
        res = await state.get_data()
        await message.answer(f"Well, let's summarize:\n"
                             f"Name: {res['name']}\n"
                             f"Surname: {res['surname']}\n"
                             f"Age: {res['age']} years")
        await state.clear()
    else:
        await message.answer(f"You try to cheat me, {message.from_user.full_name}?\n"
                             f"Enter your real age.")
