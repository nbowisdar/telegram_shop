import asyncio
from datetime import date
from pprint import pprint

from loguru import logger
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile
import multiprocessing as ml
from config import owners_id
from setup import bot
from asyncio import sleep
from src.database.crud.get import get_all_users_stat, get_all_stat
from src.telegram.messages.admin_msg import build_all_new_users_stat_msg, build_all_stat_msg


async def _send_backup():
    # stat = get_all_stat()
    # msg = build_all_new_users_stat_msg(stat)
    msg = build_all_stat_msg()
    db = FSInputFile("app.db", filename=f"backup {date.today()}")
    for owner_id in owners_id:
        try:
            await bot.send_document(owner_id, document=db, caption=msg)
        except TelegramBadRequest:
            logger.info(f"Не можу відправити бекап - {owner_id}")


async def sending_backup(sleep_sec=86400):
    while True:
        logger.info(f"Send backup after {sleep_sec} sec.")
        await asyncio.sleep(sleep_sec)
        await _send_backup()


def run_async_function_in_process():
    # Create a new event loop in the new process
    loop = asyncio.new_event_loop()
    # loop.
    # asyncio.set_event_loop(loop)
    # Run the async function within the event loop
    loop.run_until_complete(sending_backup())


def sending_backup_sync():
    proc = ml.Process(target=run_async_function_in_process)
    proc.start()

