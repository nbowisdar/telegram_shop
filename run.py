from setup import bot, dp
from src.telegram.handlers.user_handlers import user_router
from src.telegram.handlers.admin_handlers import admin_router
import asyncio
from loguru import logger


async def _start():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


def start_bot():
    asyncio.run(_start())


if __name__ == '__main__':
    logger.info("Bot started")
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")