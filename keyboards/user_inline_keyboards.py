from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

initial_keyboard_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Побывать Дедом Морозом', callback_data='judge')],
        [InlineKeyboardButton(text='Погадай', callback_data='divine')],
        [InlineKeyboardButton(text='Послание в будущее', callback_data='future')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)


coal_or_gift_keyboard_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подарок', callback_data='gift')],
        [InlineKeyboardButton(text='Уголёк', callback_data='coal')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)

yes_or_cancel_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='more')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)


set_or_show_future_message = InlineKeyboardMarkup(
    inline_keyboard =[
        [InlineKeyboardButton(text='Написать сообщение в будущее', callback_data='set_future')],
        [InlineKeyboardButton(text='Посмотреть своё сообщение в будущее', callback_data='show_future_message')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)

