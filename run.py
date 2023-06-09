from setup import bot, dp
from src.database.tables import create_table
from src.telegram.handlers.user_handlers import user_router
from src.telegram.handlers.admin_handlers import admin_router
from src.telegram.handlers.order_handlers import order_router
import asyncio
from loguru import logger

from src.telegram.middleware.admin_only import AdminOnly
from src.telegram.middleware.check_bot_online import CheckOnline


async def _start():
    admin_router.message.middleware(AdminOnly())
    user_router.message.middleware(CheckOnline())
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(order_router)
    await dp.start_polling(bot)


def start_bot():
    create_table()
    asyncio.run(_start())


if __name__ == '__main__':
    logger.info("Bot started")
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")