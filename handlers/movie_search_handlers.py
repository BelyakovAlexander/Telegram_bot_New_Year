import requests
from pprint import pprint
from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import movie_search_kbd, limit_choose_keyboard, limit_set_callbacks, history_keyboard
from loader import user_router
from states.user_states import MovieSearch
from config_data.config import API_KEY
from database.engine import save_request, set_limit, get_user_limit, get_history


@user_router.message(StateFilter(None), F.text.lower() == 'movie search')
async def bot_quiz(message: types.Message, state: FSMContext) -> None:
    """Handler to start movies search"""
    await message.answer(f"Ok, {message.from_user.full_name}.\nPlease, choose one of the sorting option: ",
                         reply_markup=movie_search_kbd)
    await state.set_state(MovieSearch.sort_option)


async def send_movies_info(message: Message, data: dict, budget = False):
    """Function for display search results in bot chat"""
    for movie in data['docs']:
        genre = ', '.join([i['name'] for i in movie['genres']]) if movie['genres'][
            0] else 'Unknown genre'  # get list of genres from movie's data

        await message.answer(f"""
    Title: {movie['alternativeName']}
    RusTitle: {movie['name']}
    Genre: {genre}
    Country: {movie['countries'][0]['name'] or 'Unknown country'}
    Year: {movie['year']}
    IMDB rating: {movie['rating']['imdb'] or 'No ratings'}
    Description: {movie['description'] or 'No description'}
    Poster: {movie['poster']['previewUrl'] or 'No poster'}
    Budget: {movie['budget']['value'] if budget else 'No budget'}""")

    # Age rating: {int(movie['ageRating']) or 'No age rating'}           # excepted because it may be NULL (not None). Fuck it.

async def send_movies_info_callback(callback: CallbackQuery, data: dict):  # NEED TO SIMPLIFY (merge with above)
    """Function for display search results in bot chat"""
    for movie in data['docs']:
        genre = ', '.join([i['name'] for i in movie['genres']]) if movie['genres'][
            0] else 'Unknown genre'  # get list of genres from movie's data

        await callback.message.answer(f"""
    Title: {movie['alternativeName']}
    RusTitle: {movie['name']}
    Genre: {genre}
    Age rating: {movie['ageRating'] or 'No age rating'}
    Country: {movie['countries'][0]['name'] or 'Unknown country'}
    Year: {movie['year']}
    IMDB rating: {movie['rating']['imdb'] or 'No ratings'}
    Description: {movie['description'] or 'No description'}
    Poster: {movie['poster']['previewUrl'] or 'No poster'}""")


@user_router.message(MovieSearch.sort_option, F.text)
async def set_search_params(message: Message, state: FSMContext) -> None:
    """Changing user's state in accordance with options he selected"""
    if message.text.lower() == 'by name':
        await message.answer('Enter movie\'s title: ')
        await state.set_state(MovieSearch.by_name)

    elif message.text.lower() == 'by rating':
        await message.answer('Sort by rating. High ratings first? Y/N ')
        await state.set_state(MovieSearch.by_rating)

    elif message.text.lower() == 'by budget':
        await message.answer('Sort by budget. High budget first? Y/N ')
        await state.set_state(MovieSearch.by_budget)

    elif message.text.lower() == 'set results limit':
        await message.answer('Select results limit: ',
                             reply_markup=limit_choose_keyboard)
        await state.set_state(MovieSearch.set_limit)

    elif message.text.lower() == 'my requests history':
        history = await get_history(message.from_user)                      # Getting user's history from database
        await message.answer('Here is your history: ',
                             reply_markup=await history_keyboard(history))
        await state.set_state(MovieSearch.history_state)

    else:
        await message.answer('I don\'t understand. Please, choose one of the options')


@user_router.message(StateFilter(MovieSearch.by_name, MovieSearch.by_rating, MovieSearch.by_budget), F.text)
async def by_name_or_rating(message: Message, state: FSMContext) -> None:
    """Movie search by title via API"""
    print('IT WORKS! ')  # TEST
    if await state.get_state() == MovieSearch.by_name:
        print(f'HERE is state BY NAME: {state}')  # TEST
        url = "https://api.kinopoisk.dev/v1.4/movie/search"

    elif await state.get_state() == MovieSearch.by_rating:
        print(f'HERE is state BY RATING: {state}')  # TEST
        url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=alternativeName&" \
              "selectFields=name&selectFields=ageRating&selectFields=genres&selectFields=countries&" \
              "selectFields=year&selectFields=rating&selectFields=description&selectFields=poster&" \
              "notNullFields=poster.url&sortField=rating.imdb&sortType=-1"

    elif await state.get_state() == MovieSearch.by_budget:
        print(f'HERE IS STATE BY BUDGET: {state}')
        url = "https://api.kinopoisk.dev/v1.4/movie?selectFields=name&selectFields=alternativeName" \
        "&selectFields=description&selectFields=type&selectFields=year&selectFields=rating&selectFields=budget" \
        "&selectFields=genres&selectFields=countries&selectFields=poster&selectField=ageRating" \
        "&notNullFields=ageRating&notNullFields=budget.value&notNullFields=poster.url&sortField=budget.value&sortType=-1"

    user_limit = await get_user_limit(message.from_user)                # take user's results length from database

    if await state.get_state() == MovieSearch.by_name or message.text.lower() in ('y', 'n'):

        params = {
            "page": 1,
            "limit": user_limit,
            "query": message.text if await state.get_state() == MovieSearch.by_name else None,

            "sortField": 'rating.imdb' if await state.get_state() == MovieSearch.by_rating
                        else 'budget.value'if await state.get_state() == MovieSearch.by_budget else None,

            "sortType": '-1'
            if await state.get_state() in (MovieSearch.by_rating, MovieSearch.by_budget) and message.text.lower() == 'y'
                        else '1'
            if await state.get_state() in (MovieSearch.by_rating, MovieSearch.by_budget) and message.text.lower() == 'n'
                        else None
        }
        headers = {
            "accept": "application/json",
            "X-API-KEY": f"{API_KEY}"
        }


        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if await state.get_state() == MovieSearch.by_name:        # if user in 'by_name' state,save full query text in database
            await save_request(user_tg_id=message.from_user.id,
                               query_url=response.url,
                               text=message.text
                               )
        # pprint(data)
        if await state.get_state() == MovieSearch.by_budget:
            pprint(data)
            await send_movies_info(message, data, budget=True)
        else:
            await send_movies_info(message, data)                                   # send message with results in telegram-bot
        await message.answer('Anything else?', reply_markup=movie_search_kbd)
        await state.set_state(MovieSearch.sort_option)

    else:
        await message.answer('I don\'t understand you. Please enter Y or N')

# _________________________________________________________________________________________________________________

@user_router.callback_query(MovieSearch.set_limit)
async def setlimit(callback: CallbackQuery, state: FSMContext):
    """Handler for changing number of displayed search results. For one certain user"""

    await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it

    await callback.message.answer(
        f'You have limited the number of displayed results to {limit_set_callbacks[callback.data]} movies')
    await set_limit(callback.from_user, new_limit=limit_set_callbacks[callback.data])
    await state.set_state(MovieSearch.sort_option)


@user_router.message(MovieSearch.set_limit)
async def wrong_limit(message: Message):
    """If user insert wrong data for limit"""
    await message.answer('Please, choose one of the given options', reply_markup=limit_choose_keyboard)


# _______________________________________________________________________________________________________________


@user_router.callback_query(MovieSearch.history_state)
async def get_history_query(callback: CallbackQuery, state: FSMContext):
    """Handler to repeat query from user history"""

    await callback.answer('')  # trick to avoid Inline button 'shining' after pushing on it

    history = await get_history(callback.from_user)  # Getting user's history from database
    num = int(callback.data[-1])
    query = history[num][2]

    headers = {
        "accept": "application/json",
        "X-API-KEY": f"{API_KEY}"
    }

    response = requests.get(url=query, headers=headers)
    data = response.json()

    await send_movies_info_callback(callback, data)  # send message with results in telegram-bot
    await callback.message.answer('Anything else?', reply_markup=movie_search_kbd)
    await state.set_state(MovieSearch.sort_option)
