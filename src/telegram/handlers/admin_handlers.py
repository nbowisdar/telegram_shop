from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command
from aiogram import F

from src.database.queries import generate_new_code
from src.telegram.buttons import admin_main_kb
from setup import admin_router, admins
from setup import bot


@admin_router.message((F.text == "/admin") & (F.from_user.id.in_(admins)))
async def main(message: Message):
    await message.answer("Вы на главной странице.",
                         reply_markup=admin_main_kb)


@admin_router.message((F.text == 'Создать промокод') & (F.from_user.id.in_(admins)))
async def create_promo(message: Message):
    new_cod = generate_new_code()
    await message.reply(f'Вы создали новый промокод - `{new_cod}`',
                        reply_markup=admin_main_kb,
                        parse_mode="MARKDOWN")


@admin_router.callback_query(Text(text="confirm"))
async def get_new_order(query: CallbackQuery):
    msg = f"{query.message.text}\n✅Подтвержденно✅"
    user_id = query.message.text.split(" ")[1]
    await query.message.edit_text(msg)
    t = "Ваш заказ подтвержден!\n В течении часа с вами свяжеться наш менеджер."
    await bot.send_message(user_id, t)
    await query.answer()


@admin_router.callback_query(Text(text="cancel"))
async def get_new_order(query: CallbackQuery):
    msg = f"{query.message.text}\n❌Откланено❌"
    user_id = query.message.text.split(" ")[1]
    await query.message.edit_text(msg)
    t = "Ваш заказ был откланен, если у вас остались вопросы\n" \
        "вы можете обратиться в нашу поддержку."
    await bot.send_message(user_id, t)
    await query.answer()
