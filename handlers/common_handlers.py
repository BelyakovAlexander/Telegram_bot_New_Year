from aiogram import F, types
from aiogram.fsm.context import FSMContext

from loader import user_router
from keyboards import initial_keyboard_inline


@user_router.message(F.photo)
async def bot_echo_photo(message: types.Message) -> None:
    await message.reply(f"Отличное изображение! Только я пока умею работать только с текстом. )")


# Echo handlers for undescribed messages
@user_router.message(F.text)
async def bot_echo(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Что-то не разберу...\n{message.text}  ?\nПопробуй нажать на одну из предложенных кнопок.",
                         reply_markup=initial_keyboard_inline)
    await state.clear()