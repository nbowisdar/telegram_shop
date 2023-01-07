from aiogram.types import Message

from src.database.queries import get_all_accounts
from src.schemas import OrderModel


def show_accounts_price() -> str:
    msg = "Все доступные аккаунты\n"
    accounts = get_all_accounts()
    for acc in accounts:
        msg += f"{acc.name} - {acc.price} руб.\n"
    return msg


def show_order(order: OrderModel) -> str:
    msg = f"""
Информация про заказ:
id заказчика - `{order.user_id}`
Товар - *{order.account_name}*
Город - *{order.city}*
Пол - *{order.sex}*
          """
    return msg