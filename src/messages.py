from aiogram.types import Message

from src.schemas import AddressModel


# from src.database.queries import get_all_accounts
# from src.schemas import OrderModel


def build_address_msg(address: AddressModel) -> str:
    return f"Ваше імя"


def show_order(order) -> str:
    if order.with_discount:
        price = f"*{round(order.account_price / 100 * 80, 2)}* руб.\nСКИДКА - {round(order.account_price / 100 * 20, 2)}"
    else:
        price = order.account_price
    msg = f"""
id заказчика - [{order.user_id}](tg://user?id={order.user_id})
Username - `@{order.account_username}`
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
