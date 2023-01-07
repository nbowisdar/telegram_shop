from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb1 = [
    [KeyboardButton(text="Отмена")]
]


cancel_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)