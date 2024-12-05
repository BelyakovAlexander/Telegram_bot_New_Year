from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# limit_set_callbacks = {'lim_2': 2, 'lim_5': 5, 'lim_10': 10, 'lim_20': 20, 'lim_40': 30}

# keyboard with automatically created buttons from dictionary 'limit_set_callbacks'
# limit_choose_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text=f'{limit_set_callbacks[i]} results', callback_data = i) for i in limit_set_callbacks
#             ]
#     ]
# )

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

# async def history_keyboard(hist_list: list):
#     """Creating of inline keyboard with user's request history
#     Callbacks are like 'hist_0', 'hist_1', 'hist_2' e.t.c."""
#     keyboard = InlineKeyboardBuilder()
#     num = 0
#     for line in hist_list:
#         clb_data = f'hist_{num}'
#         keyboard.add(InlineKeyboardButton(
#             text=f'{line[0]}',
#             callback_data=clb_data)
#         )
#         num += 1
#     return keyboard.adjust(2).as_markup()
