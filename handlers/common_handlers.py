from aiogram import F, types

from loader import user_router


@user_router.message(F.photo)
async def bot_echo_photo(message: types.Message) -> None:
    await message.reply(f"Отличное изображение! Только я пока умею работать только с текстом. )")


# Echo handlers for undescribed messages
@user_router.message(F.text)
async def bot_echo(message: types.Message) -> None:
    await message.answer(f"Что-то не разберу...\n{message.text}  ?")