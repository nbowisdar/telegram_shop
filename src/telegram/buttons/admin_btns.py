from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb1 = [
    [KeyboardButton(text="Заказы"), KeyboardButton(text="Создать промокод")]
]


admin_main_kb = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)