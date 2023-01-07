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
    if order.with_discount:
        price = f"*{round(order.account_price / 100 * 80, 2)}* руб.\nСКИДКА - {round(order.account_price / 100 * 20, 2)}"
    else:
        price = order.account_price
    msg = f"""
Информация про заказ:
id заказчика - `{order.user_id}`
Товар - *{order.account_name}* 
Цена - {price} руб.
Город - *{order.city}*
Пол - *{order.sex}*
"""
    if order.car:
        msg += f"Машина - *{order.car}*\n"
    if order.note:
        msg += f"Коментарий - {order.note}\n"
    return msg
