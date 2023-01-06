from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from setup import user_router


@user_router.message(Command(commands='start'))
async def test(message: Message):
    await message.answer("bot works")


@user_router.message(F.text == 'test')
async def test(message: Message):
    await message.answer("bot works")