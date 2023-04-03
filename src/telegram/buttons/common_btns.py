from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


cancel_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Відмінити")]],
    resize_keyboard=True
)