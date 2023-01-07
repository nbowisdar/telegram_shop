from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from src.telegram.buttons import admin_main_kb
from setup import admin_router, admins


@admin_router.message((F.text == "/admin") & (F.from_user.id.in_(admins)))
async def main(message: Message):
    await message.answer("Вы на главной странице.",
                         reply_markup=admin_main_kb)
