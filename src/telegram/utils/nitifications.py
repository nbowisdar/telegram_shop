from config import admins
from setup import bot
from src.database.tables import Order
from src.telegram.buttons import confirm_order_inl


async def send_confirmation_to_admin(msg: str):
    for admin_id in admins:
        await bot.send_message(admin_id, msg, parse_mode="MARKDOWN",
                               reply_markup=confirm_order_inl)
