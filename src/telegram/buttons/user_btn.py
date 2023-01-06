from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


"""
1) цена Аккаунтов
2) Купить аккаунт
3) Тех поддержка
4) наш канал
"""


kb1 = [
    [KeyboardButton(text="Цена Аккаунтов💸"), KeyboardButton(text="Купить аккаунт⚡️")],
    [KeyboardButton(text="Тех поддержка💻"), KeyboardButton(text="Наш канал🎩")],
]


user_main_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)
