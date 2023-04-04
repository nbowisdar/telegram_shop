from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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