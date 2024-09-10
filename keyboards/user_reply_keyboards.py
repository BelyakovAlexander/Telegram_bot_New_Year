from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

initial_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Movie search'),
        ],
        [
            KeyboardButton(text='Info'),
            KeyboardButton(text='Feedback')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose any option',
    one_time_keyboard=False
)

del_keyboard = ReplyKeyboardRemove()