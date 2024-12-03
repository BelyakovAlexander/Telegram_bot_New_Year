import random

import requests
from pprint import pprint
from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import coal_or_gift_kbd, limit_choose_keyboard, limit_set_callbacks, history_keyboard
from loader import user_router
from states.user_states import QuizStates
from database.engine import set_limit, get_user_limit

children_actions = {'Художественное творчество на стенах: Рисунки на обоях, стенах или мебели фломастерами': 'уголёк',
                'Исследование пространства: Полное исследование чужого дома, заглядывание в шкафы и ящики': 'уголёк',
                'Игры с игрушками: Использование чужих игрушек совершенно неожиданным способом или без спроса': 'уголёк',
                'Разливание воды, купание игрушек в тазике или ведре, приводящее к образованию луж на полу': 'уголёк',

                'Забавные и неожиданные места для пряток, от которых родители приходят в восторг (иногда – в ужас)': 'подарок',
                'Смешные рисунки: Рисует необычные и забавные картинки, которые могут быть не очень похожи на реальность, но полны детского очарования': 'подарок',
                'Забавная мимика и жесты: Гримасы, смешные жесты и шутки': 'подарок',
                'Неожиданные объятия домашнего питомца, ведущие к его возмущению или радости': 'подарок',
                'Неловкие танцы: Самобытные и забавные танцы под любимую музыку': 'подарок'
                }


@user_router.message(StateFilter(None), F.text.lower() == 'оценить поступки')
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    """Handler to start movies search"""
    await message.answer(f"Ну что ж, {message.from_user.full_name}.\n"
                         f"Давай сыграем в игру: ты будешь оценивать поступки детей, выбирая, "
                         f"что бы ты подарил(а) за каждый поступок - подарок или уголёк.\n"
                         f"Готов? Если да, напиши что-нибудь! ",
                         reply_markup=coal_or_gift_kbd)
    await state.update_data(user_rating=0)
    await state.update_data(question_num=1)
    await state.set_state(QuizStates.behavior_quiz_state)


@user_router.message(QuizStates.behavior_quiz_state, F.text)
async def start_quiz(message: Message, state: FSMContext) -> None:
    """Запуск опроса о поведении детей"""
    # if message.text.lower() in ('подарок', 'уголёк'):
    if message:
        await state.update_data(question=random.choice(list(children_actions)))
        res = await state.get_data()
        await message.answer(f'{res["question"]}')
        await state.set_state(QuizStates.quiz_question)


@user_router.message(QuizStates.quiz_question, F.text)
async def quiz_question(message: Message, state: FSMContext) -> None:
    res: dict = await state.get_data()
    usr_answer: str = message.text
    await state.update_data(question_num=res['question_num'] + 1)

    await message.answer(f'Вопрос: {res["question"]}\n'
                         f'Верный ответ: {children_actions[res["question"]]}\n'
                         f'Ответ пользователя: {usr_answer}')

    if children_actions[res['question']] == 'уголёк':
        if usr_answer.lower() == 'подарок':
            await state.update_data(user_rating=res['user_rating'] + 1)
            await message.answer(f'Ты добряк')

    elif children_actions[res['question']] == 'подарок':
        if usr_answer.lower() == 'уголёк':
            await state.update_data(user_rating=res['user_rating'] - 1)
            await message.answer(f'Ты злодей')
    await message.answer(f'Рейтинг: {res["user_rating"]}\tВопрос № {res["question_num"]}')

    if res['question_num'] <= 4:
        await message.answer('Следующий вопрос?')
        await state.set_state(QuizStates.behavior_quiz_state)                   #TEST DELETED
        # await quiz_question
    else:
        await message.answer('Закончили упражнение. Хочешь узнать результаты?')
        await state.set_state(QuizStates.results_of_quiz)


@user_router.message(QuizStates.results_of_quiz, F.text)
async def results_of_quiz(message: Message, state: FSMContext) -> None:
    res: dict = await state.get_data()
    rating = res['user_rating']
    await message.answer(f'{message.md_text.capitalize()}? Хорошо!\nРейтинг: {rating}')
    kindness = 'вредный' if rating <= -2 else 'справедливый' if (-1 <= rating <= 1) else 'добрый'
    await message.answer(f'Вы {kindness} Дед Мороз!')




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


@user_router.message(QuizStates.behavior_quiz_state, F.text)
async def set_search_params(message: Message, state: FSMContext) -> None:
    """Changing user's state in accordance with options he selected"""
    if message.text.lower() == 'подарок':
        await message.answer('Тогда вот тебе первый поступок:')

        await state.set_state(QuizStates.by_name)

    elif message.text.lower() == 'by rating':
        await message.answer('Sort by rating. High ratings first? Y/N ')
        await state.set_state(QuizStates.by_rating)

    elif message.text.lower() == 'by budget':
        await message.answer('Sort by budget. High budget first? Y/N ')
        await state.set_state(QuizStates.by_budget)

    elif message.text.lower() == 'set results limit':
        await message.answer('Select results limit: ',
                             reply_markup=limit_choose_keyboard)
        await state.set_state(QuizStates.set_limit)

    elif message.text.lower() == 'my requests history':
        history = await get_history(message.from_user)                      # Getting user's history from database
        await message.answer('Here is your history: ',
                             reply_markup=await history_keyboard(history))
        await state.set_state(QuizStates.history_state)

    else:
        await message.answer('I don\'t understand. Please, choose one of the options')


@user_router.message(StateFilter(QuizStates.by_name, QuizStates.by_rating, QuizStates.by_budget), F.text)
async def by_name_or_rating(message: Message, state: FSMContext) -> None:
    """Movie search by title via API"""
    print('IT WORKS! ')  # TEST
    if await state.get_state() == QuizStates.by_name:
        print(f'HERE is state BY NAME: {state}')  # TEST
        url = "https://api.kinopoisk.dev/v1.4/movie/search"

    elif await state.get_state() == QuizStates.by_rating:
        print(f'HERE is state BY RATING: {state}')  # TEST
        url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=alternativeName&" \
              "selectFields=name&selectFields=ageRating&selectFields=genres&selectFields=countries&" \
              "selectFields=year&selectFields=rating&selectFields=description&selectFields=poster&" \
              "notNullFields=poster.url&sortField=rating.imdb&sortType=-1"

    elif await state.get_state() == QuizStates.by_budget:
        print(f'HERE IS STATE BY BUDGET: {state}')
        url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=name&selectFields=alternativeName" \
        "&selectFields=description&selectFields=type&selectFields=year&selectFields=rating&selectFields=budget" \
        "&selectFields=genres&selectFields=countries&selectFields=poster&selectField=ageRating" \
        "&notNullFields=ageRating&notNullFields=budget.value&notNullFields=poster.url&sortField=budget.value&sortType=-1"

    user_limit = await get_user_limit(message.from_user)                # take user's results length from database

    if await state.get_state() == QuizStates.by_name or message.text.lower() in ('y', 'n'):

        params = {
            "page": 1,
            "limit": user_limit,
            "query": message.text if await state.get_state() == QuizStates.by_name else None,

            "sortField": 'rating.imdb' if await state.get_state() == QuizStates.by_rating
                        else 'budget.value'if await state.get_state() == QuizStates.by_budget else None,

            "sortType": '-1'
            if await state.get_state() in (QuizStates.by_rating, QuizStates.by_budget) and message.text.lower() == 'y'
                        else '1'
            if await state.get_state() in (QuizStates.by_rating, QuizStates.by_budget) and message.text.lower() == 'n'
                        else None
        }
        headers = {
            "accept": "application/json"
        }


        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if await state.get_state() == QuizStates.by_name:        # if user in 'by_name' state,save full query text in database
            await save_request(user_tg_id=message.from_user.id,
                               query_url=response.url,
                               text=message.text
                               )
        # pprint(data)
        if await state.get_state() == QuizStates.by_budget:
            pprint(data)
            await send_movies_info(message, data, budget=True)
        else:
            await send_movies_info(message, data)                                   # send message with results in telegram-bot
        await message.answer('Anything else?', reply_markup=coal_or_gift_kbd)
        await state.set_state(QuizStates.behavior_quiz_state)

    else:
        await message.answer('I don\'t understand you. Please enter Y or N')

# _________________________________________________________________________________________________________________

@user_router.callback_query(QuizStates.set_limit)
async def setlimit(callback: CallbackQuery, state: FSMContext):
    """Handler for changing number of displayed search results. For one certain user"""

    await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it

    await callback.message.answer(
        f'You have limited the number of displayed results to {limit_set_callbacks[callback.data]} movies')
    await set_limit(callback.from_user, new_limit=limit_set_callbacks[callback.data])
    await state.set_state(QuizStates.behavior_quiz_state)


@user_router.message(QuizStates.set_limit)
async def wrong_limit(message: Message):
    """If user insert wrong data for limit"""
    await message.answer('Please, choose one of the given options', reply_markup=limit_choose_keyboard)


# _______________________________________________________________________________________________________________


@user_router.callback_query(QuizStates.history_state)
async def get_history_query(callback: CallbackQuery, state: FSMContext):
    """Handler to repeat query from user history"""

    await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it

    history = await get_history(callback.from_user)  # Getting user's history from database
    num = int(callback.data[-1])
    query = history[num][2]

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url=query, headers=headers)
    data = response.json()

    await send_movies_info_callback(callback, data)  # send message with results in telegram-bot
    await callback.message.answer('Anything else?', reply_markup=coal_or_gift_kbd)
    await state.set_state(QuizStates.behavior_quiz_state)
