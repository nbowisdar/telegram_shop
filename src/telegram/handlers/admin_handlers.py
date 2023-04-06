from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram import F

from src.database.promo_queries import generate_new_code
from src.telegram.buttons import admin_main_kb, admin_goods_kb, admin_cancel_btn
from setup import admin_router
from setup import bot
from src.telegram.handlers.fsm_h.admin_fsm.add_promo_fsm import PromoCodeState
from src.telegram.handlers.fsm_h.admin_fsm.goods.add_goods import GoodsState
from src.telegram.handlers.fsm_h.admin_fsm.goods.update_goods import UpdateAddr


@admin_router.message(F.text.in_(["/admin", "⬅️ На головну"]))
async def main(message: Message):
    await message.answer("Ти адмін!",
                         reply_markup=admin_main_kb)


# @admin_router.message(F.text == '🔑 Створити новий промокод')
# async def create_promo(message: Message):
#     new_cod = generate_new_code()
#     await message.reply(f'Ви створили новий промокод - `{new_cod}`',
#                         reply_markup=admin_main_kb,
#                         parse_mode="MARKDOWN")


@admin_router.message(F.text == '🛍 Товари')
async def create_promo(message: Message):
    await message.reply(f'Розділ: Товари', reply_markup=admin_goods_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == "✏️ Додати")
async def add_goods(message: Message, state: FSMContext):
    await message.answer("Введіть назву товару", reply_markup=admin_cancel_btn)
    await state.set_state(GoodsState.name)


# @admin_router.message(F.text == "🔨 Оновити")
# async def add_goods(message: Message, state: FSMContext):
#     await message.answer("Введіть назву товару", reply_markup=admin_cancel_btn)
#     await state.set_state(UpdateAddr.field)


@admin_router.message(F.text == "🔑 Створити новий промокод")
async def new_code(message: Message, state: FSMContext):
    await state.set_state(PromoCodeState.max_use)
    await message.answer("Введіть число, скільки разів можно використати цей промокод",
                         reply_markup=ReplyKeyboardRemove())


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
