from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from setup import user_router
from src.telegram.buttons import user_main_btn
from setup import bot


@user_router.message(Command(commands='start'))
async def test(message: Message):
    await message.answer("bot works",
                         reply_markup=user_main_btn)


