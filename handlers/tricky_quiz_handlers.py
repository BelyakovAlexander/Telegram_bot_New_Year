import random

import requests
from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import coal_or_gift_keyboard_inline, yes_or_cancel_inline, initial_keyboard_inline
from loader import user_router
from states.user_states import QuizStates

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
@user_router.callback_query(StateFilter(None), F.data == 'judge')
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
