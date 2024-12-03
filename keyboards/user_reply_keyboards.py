from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

initial_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оценить поступки')
        ],
        [
            KeyboardButton(text='Погадай'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите один из вариантов',
    one_time_keyboard=False
)

# клавиатура для ответов на вопросы об оценке поступка ребёнка
coal_or_gift_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подарок'),
            KeyboardButton(text='Уголёк')
        ],
        [KeyboardButton(text='Отмена')
         ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выбери, что ты подаришь ребёнку за это',
    one_time_keyboard=False
)

# if it is necessary to remove the keyboard
del_keyboard = ReplyKeyboardRemove()