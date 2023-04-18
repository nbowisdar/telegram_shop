import types
from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
import json

default_settings = {
    "online": False,
    "pay_card": False
}


def get_or_generate_settings() -> dict:
    try:
        with open("settings.json", mode='r', encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        with open("settings.json", mode='w', encoding="utf-8") as file:
            json.dump(default_settings, file)


def get_status() -> bool:
    return settings['online']
    # try:
    #     with open("settings.json", mode='r', encoding="utf-8") as file:
    #         data = json.load(file)
    #         return data['online']
    # except FileNotFoundError:
    #     return False


def change_status_bot():
    online = get_status()
    if online:
        settings["online"] = False
    else:
        settings["online"] = True

    with open("settings.json", mode='w', encoding="utf-8") as file:
        json.dump(settings, file)


def get_status_pay_card() -> bool:
    return settings['pay_card']


def change_status_pay_card():
    online = get_status_pay_card()
    if online:
        settings["pay_card"] = False
    else:
        settings["pay_card"] = True

    with open("settings.json", mode='w', encoding="utf-8") as file:
        json.dump(settings, file)


settings = get_or_generate_settings()

load_dotenv()
TOKEN = os.getenv("TOKEN")
NOVA_POST = os.getenv("NOVA_POST")

BASE_URL_NP = "https://api.novaposhta.ua/v2.0/json/"

bot = Bot(TOKEN, parse_mode="MARKDOWN")
dp = Dispatcher()

# create routes

admin_router = Router()
user_router = Router()
order_router = Router()
# common_router = Router()

BASE_DIR = os.path.dirname(__file__)