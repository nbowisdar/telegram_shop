from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command
from aiogram import F

from src.database.queries import generate_new_code
from src.telegram.buttons import admin_main_kb
from setup import admin_router, admins
from setup import bot


@admin_router.message(F.text == "/admin")
async def main(message: Message):
    await message.answer("Ти адмін!",
                         reply_markup=admin_main_kb)


@admin_router.message(F.text == 'Створити новий промокод')
async def create_promo(message: Message):
    new_cod = generate_new_code()
    await message.reply(f'Ви створили новий промокод - `{new_cod}`',
                        reply_markup=admin_main_kb,
                        parse_mode="MARKDOWN")


@admin_router.callback_query(Text(text="confirm"))
async def get_new_order(query: CallbackQuery):
    msg = f"{query.message.text}\n✅Підтвердженно✅"
    user_id = query.message.text.split(" ")[1]
    await query.message.edit_text(msg)
    t = "Ваше замовлення підтверджено!\n Протягом години з вами зв'яжеться наш менеджер."
    await bot.send_message(user_id, t)
    await query.answer()


@admin_router.callback_query(Text(text="cancel"))
async def get_new_order(query: CallbackQuery):
    msg = f"{query.message.text}\n❌Відхилено❌"
    user_id = query.message.text.split(" ")[1]
    await query.message.edit_text(msg)
    t = "Ваше замовлення було відхилено, якщо у вас залишилися питання\n" \
         "Ви можете звернутися на нашу підтримку."
    await bot.send_message(user_id, t)
    await query.answer()
