import random

import requests
from pprint import pprint
from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import coal_or_gift_keyboard_inline, yes_or_cancel_inline, initial_keyboard_inline
from loader import user_router
from states.user_states import QuizStates
from database.engine import set_limit, get_user_limit

                                                                                                                                #TODO
# children_actions = {'Художественное творчество на стенах: Рисунки на обоях, стенах или мебели фломастерами': 'уголёк',
#                 'Исследование пространства: Полное исследование чужого дома, заглядывание в шкафы и ящики': 'уголёк',
#                 'Игры с игрушками: Использование чужих игрушек совершенно неожиданным способом или без спроса': 'уголёк',
#                 'Разливание воды, купание игрушек в тазике или ведре, приводящее к образованию луж на полу': 'уголёк',
#
#                 'Забавные и неожиданные места для пряток, от которых родители приходят в восторг (иногда – в ужас)': 'подарок',
#                 'Смешные рисунки: Рисует необычные и забавные картинки, которые могут быть не очень похожи на реальность, но полны детского очарования': 'подарок',
#                 'Забавная мимика и жесты: Гримасы, смешные жесты и шутки': 'подарок',
#                 'Неожиданные объятия домашнего питомца, ведущие к его возмущению или радости': 'подарок',
#                 'Неловкие танцы: Самобытные и забавные танцы под любимую музыку': 'подарок'
#                 }

children_actions = {'Художественное творчество на стенах: Рисунки на обоях, стенах или мебели фломастерами': 'coal',
                'Исследование пространства: Полное исследование чужого дома, заглядывание в шкафы и ящики': 'coal',
                'Игры с игрушками: Использование чужих игрушек совершенно неожиданным способом или без спроса': 'coal',
                'Разливание воды, купание игрушек в тазике или ведре, приводящее к образованию луж на полу': 'coal',
                'Рассказывание всем секретов, доверенных другом или подругой': 'coal',
                'Разбирание чужих вещей в целях разобраться в их внутреннем устройстве': 'coal',

                'Забавные и неожиданные места для пряток, от которых родители приходят в восторг (иногда – в ужас)': 'gift',
                'Смешные рисунки: Рисует необычные и забавные картинки, которые могут быть не очень похожи на реальность, но полны детского очарования': 'gift',
                'Забавная мимика и жесты: Гримасы, смешные жесты и шутки': 'gift',
                'Неожиданные объятия домашнего питомца, ведущие к его возмущению или радости': 'gift',
                'Неловкие танцы: Самобытные и забавные танцы под любимую музыку': 'gift',
                'Неожиданные сюрпризы: Изготовить что-то своими руками, чтобы порадовать друзей или близких' : 'gift',
                'Загадочные фокусы: Удивить окружающих потрясающим волшебным трюком': 'gift',
                'Окунуться в фантазию: Рассматривать картинки в книге и представлять себя внутри сказки': 'gift'
                }


# @user_router.message(StateFilter(None), F.text.lower() == 'оценить поступки')
@user_router.callback_query(StateFilter(None), F.data)
async def bot_quiz(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер для начала опроса по оценке поступков
    """
    await callback.message.answer(f'Давай сыграем в игру <b>"Какой ты Дед Мороз"</b>: '
                         f'я буду отправлять поступок ребенка, а ты, как Дед Мороз, будешь оценивать, '
                         f'что заслужил этот ребенок в этом году: подарок или уголек. Начинаем?',
                                  reply_markup=yes_or_cancel_inline)
    await state.update_data(user_rating=0)
    await state.update_data(question_num=1)
    await state.set_state(QuizStates.behavior_quiz_state)


# @user_router.message(QuizStates.behavior_quiz_state, F.text)
@user_router.callback_query(QuizStates.behavior_quiz_state, F.data)            # test if F.data not defined - will it work?  == ('more', 'gift', 'coal')
# async def start_quiz(message: Message, state: FSMContext) -> None:
async def start_quiz(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Запуск опроса о поведении детей"""
    await state.update_data(question=random.choice(list(children_actions)))
    res = await state.get_data()
    await callback.message.answer(f'{res["question"]}', reply_markup=coal_or_gift_keyboard_inline)
    await state.set_state(QuizStates.quiz_question)


# @user_router.message(QuizStates.quiz_question, F.text)
@user_router.callback_query(QuizStates.quiz_question, F.data)
# async def quiz_question(message: Message, state: FSMContext) -> None:
async def quiz_question(callback: types.CallbackQuery, state: FSMContext) -> None:
    res: dict = await state.get_data()
    # usr_answer: str = message.text                                    # TEST - REPLACED LINE
    usr_answer: str = callback.data
    await state.update_data(question_num=res['question_num'] + 1)

    await callback.message.answer(f'Вопрос: {res["question"]}\n'                                        # TEST
                         f'Верный ответ: {children_actions[res["question"]]}\n'                         # TEST
                         f'Ответ пользователя: {usr_answer}')                                           # TEST

    if children_actions[res['question']] == 'coal':
        if usr_answer.lower() == 'gift':
            await state.update_data(user_rating=res['user_rating'] + 1)                                  # TEST
            await callback.message.answer(f'Ты добряк')                                                  # TEST

    elif children_actions[res['question']] == 'gift':
        if usr_answer.lower() == 'coal':
            await state.update_data(user_rating=res['user_rating'] - 1)
            await callback.message.answer(f'Ты злодей')                                                     # TEST
    await callback.message.answer(f'Рейтинг: {res["user_rating"]}\tВопрос № {res["question_num"]}')         # TEST

    if res['question_num'] <= 4:
        await callback.message.answer('Записал... Следующий вопрос?', reply_markup=yes_or_cancel_inline)
        await state.set_state(QuizStates.behavior_quiz_state)
        # await quiz_question
    else:
        await callback.message.answer('Это был последний вопрос. Хочешь узнать результаты?', reply_markup=yes_or_cancel_inline)
        await state.set_state(QuizStates.results_of_quiz)


# хендлер в случае, если пользователь введёт текст при запросе следующего вопроса или начале игры
@user_router.message(StateFilter(QuizStates.behavior_quiz_state, QuizStates.quiz_question), F.text)
async def quiz_question_error(message: Message, state: FSMContext) -> None:
    now_state = await state.get_state()
    if now_state == 'QuizStates:behavior_quiz_state':
        keyboard = yes_or_cancel_inline
    else:
        keyboard = coal_or_gift_keyboard_inline
    await message.answer('Извини, но я лищь бот, и в этом опросе могу общаться только через нажатия кнопок.'
                         ' Выбери, пожалуйста, верный ответ:', reply_markup=keyboard)


@user_router.callback_query(QuizStates.results_of_quiz, F.data == 'more')
# async def results_of_quiz(message: Message, state: FSMContext) -> None:
async def results_of_quiz(callback: types.CallbackQuery, state: FSMContext) -> None:
    res: dict = await state.get_data()
    rating = res['user_rating']
    await callback.message.answer(f'Хорошо!\nРейтинг: {rating}')
    kindness = 'вредный' if rating <= -2 else 'справедливый' if -1 <= rating <= 1 else 'добрый'
    kind_reply = 'Детям сложно получмть от тебя подарки' if rating <= -2 \
        else 'Ты правильно выбираешь вознаграждения для детей - они будут стараться вести себя хорошо!' if -1 <= rating <= 1\
        else 'Ты очень любишь детей, и прощаешь им любые шалости!'
    await callback.message.answer(f'Ты {kindness} Дед Мороз! {kind_reply}', reply_markup=initial_keyboard_inline)
    await state.clear()




# async def send_movies_info(message: Message, data: dict, budget = False):
#     """Function for display search results in bot chat"""
#     for movie in data['docs']:
#         genre = ', '.join([i['name'] for i in movie['genres']]) if movie['genres'][
#             0] else 'Unknown genre'  # get list of genres from movie's data
#
#         await message.answer(f"""
#     Title: {movie['alternativeName']}
#     RusTitle: {movie['name']}
#     Genre: {genre}
#     Country: {movie['countries'][0]['name'] or 'Unknown country'}
#     Year: {movie['year']}
#     IMDB rating: {movie['rating']['imdb'] or 'No ratings'}
#     Description: {movie['description'] or 'No description'}
#     Poster: {movie['poster']['previewUrl'] or 'No poster'}
#     Budget: {movie['budget']['value'] if budget else 'No budget'}""")


# async def send_movies_info_callback(callback: CallbackQuery, data: dict):  # NEED TO SIMPLIFY (merge with above)
#     """Function for display search results in bot chat"""
#     for movie in data['docs']:
#         genre = ', '.join([i['name'] for i in movie['genres']]) if movie['genres'][
#             0] else 'Unknown genre'  # get list of genres from movie's data
#
#         await callback.message.answer(f"""
#     Title: {movie['alternativeName']}
#     RusTitle: {movie['name']}
#     Genre: {genre}
#     Age rating: {movie['ageRating'] or 'No age rating'}
#     Country: {movie['countries'][0]['name'] or 'Unknown country'}
#     Year: {movie['year']}
#     IMDB rating: {movie['rating']['imdb'] or 'No ratings'}
#     Description: {movie['description'] or 'No description'}
#     Poster: {movie['poster']['previewUrl'] or 'No poster'}""")


# @user_router.message(QuizStates.behavior_quiz_state, F.text)
# async def set_search_params(message: Message, state: FSMContext) -> None:
#     """Changing user's state in accordance with options he selected"""
#     if message.text.lower() == 'подарок':
#         await message.answer('Тогда вот тебе первый поступок:')
#
#         await state.set_state(QuizStates.by_name)
#
#     elif message.text.lower() == 'by rating':
#         await message.answer('Sort by rating. High ratings first? Y/N ')
#         await state.set_state(QuizStates.by_rating)
#
#     elif message.text.lower() == 'by budget':
#         await message.answer('Sort by budget. High budget first? Y/N ')
#         await state.set_state(QuizStates.by_budget)
#
#     elif message.text.lower() == 'set results limit':
#         await message.answer('Select results limit: ',
#                              reply_markup=limit_choose_keyboard)
#         await state.set_state(QuizStates.set_limit)
#
#     elif message.text.lower() == 'my requests history':
#         history = await get_history(message.from_user)                      # Getting user's history from database
#         await message.answer('Here is your history: ',
#                              reply_markup=await history_keyboard(history))
#         await state.set_state(QuizStates.history_state)
#
#     else:
#         await message.answer('I don\'t understand. Please, choose one of the options')
#
#
# @user_router.message(StateFilter(QuizStates.by_name, QuizStates.by_rating, QuizStates.by_budget), F.text)
# async def by_name_or_rating(message: Message, state: FSMContext) -> None:
#     """Movie search by title via API"""
#     print('IT WORKS! ')  # TEST
#     if await state.get_state() == QuizStates.by_name:
#         print(f'HERE is state BY NAME: {state}')  # TEST
#         url = "https://api.kinopoisk.dev/v1.4/movie/search"
#
#     elif await state.get_state() == QuizStates.by_rating:
#         print(f'HERE is state BY RATING: {state}')  # TEST
#         url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=alternativeName&" \
#               "selectFields=name&selectFields=ageRating&selectFields=genres&selectFields=countries&" \
#               "selectFields=year&selectFields=rating&selectFields=description&selectFields=poster&" \
#               "notNullFields=poster.url&sortField=rating.imdb&sortType=-1"
#
#     elif await state.get_state() == QuizStates.by_budget:
#         print(f'HERE IS STATE BY BUDGET: {state}')
#         url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=name&selectFields=alternativeName" \
#         "&selectFields=description&selectFields=type&selectFields=year&selectFields=rating&selectFields=budget" \
#         "&selectFields=genres&selectFields=countries&selectFields=poster&selectField=ageRating" \
#         "&notNullFields=ageRating&notNullFields=budget.value&notNullFields=poster.url&sortField=budget.value&sortType=-1"
#
#     user_limit = await get_user_limit(message.from_user)                # take user's results length from database
#
#     if await state.get_state() == QuizStates.by_name or message.text.lower() in ('y', 'n'):
#
#         params = {
#             "page": 1,
#             "limit": user_limit,
#             "query": message.text if await state.get_state() == QuizStates.by_name else None,
#
#             "sortField": 'rating.imdb' if await state.get_state() == QuizStates.by_rating
#                         else 'budget.value'if await state.get_state() == QuizStates.by_budget else None,
#
#             "sortType": '-1'
#             if await state.get_state() in (QuizStates.by_rating, QuizStates.by_budget) and message.text.lower() == 'y'
#                         else '1'
#             if await state.get_state() in (QuizStates.by_rating, QuizStates.by_budget) and message.text.lower() == 'n'
#                         else None
#         }
#         headers = {
#             "accept": "application/json"
#         }
#
#
#         response = requests.get(url, headers=headers, params=params)
#         data = response.json()
#
#         if await state.get_state() == QuizStates.by_name:        # if user in 'by_name' state,save full query text in database
#             await save_request(user_tg_id=message.from_user.id,
#                                query_url=response.url,
#                                text=message.text
#                                )
#         # pprint(data)
#         if await state.get_state() == QuizStates.by_budget:
#             pprint(data)
#             await send_movies_info(message, data, budget=True)
#         else:
#             await send_movies_info(message, data)                                   # send message with results in telegram-bot
#         await message.answer('Anything else?', reply_markup=coal_or_gift_kbd)
#         await state.set_state(QuizStates.behavior_quiz_state)
#
#     else:
#         await message.answer('I don\'t understand you. Please enter Y or N')
#
# # _________________________________________________________________________________________________________________
#
# @user_router.callback_query(QuizStates.set_limit)
# async def setlimit(callback: CallbackQuery, state: FSMContext):
#     """Handler for changing number of displayed search results. For one certain user"""
#
#     await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it
#
#     await callback.message.answer(
#         f'You have limited the number of displayed results to {limit_set_callbacks[callback.data]} movies')
#     await set_limit(callback.from_user, new_limit=limit_set_callbacks[callback.data])
#     await state.set_state(QuizStates.behavior_quiz_state)
#
#
# @user_router.message(QuizStates.set_limit)
# async def wrong_limit(message: Message):
#     """If user insert wrong data for limit"""
#     await message.answer('Please, choose one of the given options', reply_markup=limit_choose_keyboard)
#
#
# # _______________________________________________________________________________________________________________
#
#
# @user_router.callback_query(QuizStates.history_state)
# async def get_history_query(callback: CallbackQuery, state: FSMContext):
#     """Handler to repeat query from user history"""
#
#     await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it
#
#     history = await get_history(callback.from_user)  # Getting user's history from database
#     num = int(callback.data[-1])
#     query = history[num][2]
#
#     headers = {
#         "accept": "application/json"
#     }
#
#     response = requests.get(url=query, headers=headers)
#     data = response.json()
#
#     await send_movies_info_callback(callback, data)  # send message with results in telegram-bot
#     await callback.message.answer('Anything else?', reply_markup=coal_or_gift_kbd)
#     await state.set_state(QuizStates.behavior_quiz_state)
