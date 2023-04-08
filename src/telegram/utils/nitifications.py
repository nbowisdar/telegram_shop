import asyncio

from aiogram.types import Message

from config import admins
from setup import bot
from src.database.tables import Order, User
from src.telegram.buttons import confirm_order_inl, admin_main_kb


async def send_confirmation_to_admin(msg: str):
    for admin_id in admins:
        await bot.send_message(admin_id, msg, parse_mode="MARKDOWN",
                               reply_markup=confirm_order_inl)


async def send_text_or_photo(*, msg: Message, user_id: int):
    print(user_id)
    if msg.photo:
        photo = msg.photo[-1].file_id
        caption = msg.caption
        await bot.send_photo(user_id, photo=photo, caption=caption)
    else:
        await bot.send_message(chat_id=user_id, text=msg.text)


async def send_to_all_users(msg: Message):
    count = 0
    for user in User.select():
        user_id = user.user_id
        if user_id not in admins:
            await send_text_or_photo(msg=msg, user_id=user.user_id)
            count += 1

    await msg.reply(f"Користувачів отримали повідомлення - {count}", reply_markup=admin_main_kb)
