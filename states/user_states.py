from aiogram.fsm.state import StatesGroup, State


class RequestInfo(StatesGroup):
    """States for user info survey"""
    name = State()



class QuizStates(StatesGroup):
    """States for movie search and sorting"""
    behavior_quiz_state = State()
    quiz_question = State()
    results_of_quiz = State()

    future_message_answer = State()

    go_to_setting_future_message = State()
    setting_future_message = State()

    show_future_message = State()
