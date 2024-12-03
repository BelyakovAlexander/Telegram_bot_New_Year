from aiogram.fsm.state import StatesGroup, State


class RequestInfo(StatesGroup):
    """States for user info survey"""
    name = State()
    # surname = State()
    # age = State()


class QuizStates(StatesGroup):
    """States for movie search and sorting"""
    behavior_quiz_state = State()
    quiz_question = State()
    results_of_quiz = State()

    set_limit = State()
    by_name = State()
    by_rating = State()
    by_budget = State()
    history_state = State()