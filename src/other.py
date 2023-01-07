from aiogram.types import Message
from setup import admins, bot


async def send_new_order_to_admin(msg: str):
    for admin in admins:
        await bot.send_message(admin, msg)