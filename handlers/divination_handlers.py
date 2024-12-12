from aiogram import types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from keyboards import del_keyboard, initial_keyboard_inline
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
                   'Тебя ждет финансовое благополучие и стабильность.',
                   'Весь следующий год будет наполнен любовью и лаской.',
                   'В новом году ты найдешь новое интересное занятие.',
                   'В новом году не бойся поступать так, как считаешь нужным!',
                   'В ближайшем будущем тебе предстоит в чем-то рискнуть. Удача на твоей стороне!',
                   'В новом году ты познакомишься с человеком, который станет тебе другом на всю жизнь.',
                   'В новом году тебя ждёт долгое путешествие, которые оправдает твои ожидания.',
                   'В Новом году открывай любые двери целеустремлённо и уверено, удача рядом.',
                   'В Новом году тебя ожидает счастливый поворот в судьбе.',
                   'В Новом году тебе выпадет шанс добиться того, о чём ты давно размышляешь.',
                   'Новый год будет наполнен приятными сюрпризами, не стоит их бояться. Наоборот, приготовься к тому, '
                        'что может потребоваться полная перезагрузка в жизни, чтобы насладиться предстоящим счастьем.',
                   'Новый год будет для тебя гармоничным. Удивительно, но наконец-то насоупит момент, когда во всех сферах'
                        'будет баланс. Тебя устроит всё, что будет происходить на работе, на личном фронте и дома.'
                        ' Окружающие заметят, как будут светиться по-новому твои глаза.',
                   'В новом году забудь о своей застенчивости! Протяни руки к своей любви и страсти!',
                   'Впереди целый год чудес, каждый месяц словно новый цветок — пусть он распустится и принесёт вам счастье!',
                   'Сбудется мечта, о которой вы давно забыли, и подарит новые краски жизни.',
                   '2025 год подарит вам людей, с которыми смех станет слаще, а тишина теплее',
                   'Этот год словно чистое полотно — возьмите кисти смелее и рисуйте жизнь, о которой мечтали.',
                   'Вам предстоит увидеть мир с новой стороны. Откройте своё сердце, чтобы идти навстречу переменам!',
                   'Новый год откроет двери, которые вы искали долго, и за ними будет то, к чему вы шли.',
                   'На ваш путь ляжет свет новой звезды, следуйте за ней, и она приведёт вас к счастью.',
                   'Год впереди — время улыбок и мудрости. Пусть каждая встреча будет шагом к вашей мечте!',
                   'Тепло, которое вы дарите, вернётся к вам с нежностью весеннего ветра.',
                   'Этот год принесет вам новые удивительные открытия! Держите глаза и сердце открытыми для маленьких чудес вокруг!',
                   'Каждый из вас в этом году найдёт новое увлечение, которое раскроет его талант и принесёт радость.',
                   'Этот год — год крепкой дружбы. Ждите новых друзей и добрых встреч.',
                   'Каждому в семье достанется по-маленькому, но важному подарку от судьбы, так что будьте готовы к сюрпризам.',
                   'В 2025 году ваш дом наполнится смехом, радостью и множеством новых достижений.',
                   'Этот год научит вас вместе побеждать любые трудности, делая семью еще сильнее и дружнее.',
                   'В 2025 году удача станет вашим постоянным спутником, помогая в важных начинаниях и неожиданных поворотах.',
                   'Пришло время получить заслуженные плоды ваших трудов — в этом году вас ждут приятные успехи!',
                   'В этом году вы ощутите истинную поддержку близких людей, и это станет вашей силой.',
                   'В 2025 году вы откроете в себе новый талант, который принесет вдохновение и новые перспективы.',
                   'Этот год наполнит вашу жизнь гармонией, позволяя найти баланс между работой и личным счастьем.'
                   )


# хендлер для начала гадания (inline)
@user_router.callback_query(StateFilter(None), F.data == 'divine')
async def bot_quiz_inline(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(f"Итак, {callback.from_user.full_name or 'дружок'}, проведём гадание!\nНапиши, пожалуйста, как тебе нравится, чтобы тебя называли? ",
                         reply_markup=del_keyboard)
    await state.set_state(RequestInfo.name)


# хендлер для начала гадания
@user_router.message(StateFilter(None), F.text.lower() == 'погадай')
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Итак, {message.from_user.full_name or 'дружок'}, проведём гадание!\nНапиши, пожалуйста, как тебе нравится, чтобы тебя называли? ",
                         reply_markup=del_keyboard)
    await state.set_state(RequestInfo.name)


@user_router.message(RequestInfo.name, F.text)
async def divination(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name = message.text)
    res = await state.get_data()
    username = res['name']
    await message.answer(username + '! ' + random.choice(divination_list), reply_markup=initial_keyboard_inline)
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
