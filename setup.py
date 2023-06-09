import types

from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
import json


def get_status() -> bool:
    try:
        with open("settings.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            return data["online"]
    except FileNotFoundError:
        return False


def change_status():
    online = get_status()
    if online:
        data = {"online": False}
    else:
        data = {"online": True}

    with open("settings.json", mode="w", encoding="utf-8") as file:
        json.dump(data, file)
        # return data['online']


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN, parse_mode="MARKDOWN")
dp = Dispatcher()

# create routes

admin_router = Router()
user_router = Router()
order_router = Router()
# common_router = Router()

BASE_DIR = os.path.dirname(__file__)
