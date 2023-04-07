from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import categories

admin_cancel_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🛑 Відмінити")]],
    resize_keyboard=True
)

admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Товари"), KeyboardButton(text="📊 Замовлення")],
        [KeyboardButton(text="🔑 Створити новий промокод")]
],
    resize_keyboard=True
)

admin_goods_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Додати"), KeyboardButton(text="🗑 Видалити"), KeyboardButton(text="🔨 Оновити")],
        [KeyboardButton(text="⬅️ На головну")]
],
    resize_keyboard=True
)


"Inline keyboards bellow"


confirm_order_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Підтвердити", callback_data="order_waiting|confirm"),
        InlineKeyboardButton(text="🛑 Відхилити", callback_data="order_waiting|decline")
    ],
])
