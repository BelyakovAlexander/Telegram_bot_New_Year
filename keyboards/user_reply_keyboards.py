from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

initial_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Movie search')
        ],
        [
            KeyboardButton(text='User info survey'),
            KeyboardButton(text='Cancel')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose any option',
    one_time_keyboard=False
)

# keyboard for movie sorting
movie_search_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='By name'),
            KeyboardButton(text='By rating')
        ],
        [
            KeyboardButton(text='By budget'),
            KeyboardButton(text='Request history'),
        ],
        [KeyboardButton(text='Set results limit')
         ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose selection option',
    one_time_keyboard=False
)

# if it is necessary to remove the keyboard
del_keyboard = ReplyKeyboardRemove()