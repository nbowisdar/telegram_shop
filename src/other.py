from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# from aiogram.utils.keyboard import InlineKeyboardBuilder

from setup import admins, bot

# builder = InlineKeyboardBuilder()
kb1 = [
    [InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
     InlineKeyboardButton(text="Отклонить", callback_data="cancel")]
]
mark = InlineKeyboardMarkup(inline_keyboard=kb1)


async def send_new_order_to_admin(msg: str, selfie: str):
    for admin in admins:
        await bot.send_photo(admin, selfie)
        await bot.send_message(admin, msg, reply_markup=mark, parse_mode="MARKDOWN")
