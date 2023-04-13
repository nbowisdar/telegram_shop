from typing import Iterable

from config import categories
from src.database.crud.get import get_all_stat
from src.database.tables import User, Goods, Order, order_status
from src.schemas import Period


def build_all_new_users_stat_msg(data: list[tuple[Period: int]]) -> str:
    return f"""
📊 Уся статистика:

    🔰 За добу - *{data[0][1]}*
    ⌚️ За неділю - *{data[1][1]}*
    🗓 За місяць - *{data[2][1]}*
    🌎 Юзерів загалом - *{data[3][1]}*
    """


def build_info_about_user(user: User):
    address = user.address.first()
    user_info = f"Id - `{user.user_id}`\nUsername - `{user.username}`\n\n"
    if address:
        addr_msg = f"Повне ім'я - *{address.full_name}*\n" \
                   f"Мобільний - *{address.mobile_number}*\n" \
                   f"Місто - *{address.city}*\n" \
                   f"Номер відділення НП - *{address.post_number}*\n\n"
    else:
        addr_msg = "Адрес не вказанно\n\n"
    order_amount = f"_Усього замовлень_ *{len(user.orders)}*"

    return user_info + addr_msg + order_amount


def build_all_stat_msg() -> str:
    users, order = get_all_stat()
    goods = Goods.select()

    return f"""
📊 СТАТИСТИКА БОТА
➖➖➖➖➖➖➖➖➖➖
┣ Юзеров за День: {users[0][1]}
┣ Юзеров за Неделю: {users[1][1]}
┣ Юзеров за Месяц: {users[2][1]}
┗ Юзеров за Всё время: {users[3][1]}

💰 Средства
┣‒ Продажи (кол-во, сумма)
┣ За День: {order[0][1][1]}шт - {order[2][1][0]} ₴
┣ За Неделю: {order[1][1][1]}шт - {order[2][1][0]} ₴
┣ За Месяц: {order[2][1][1]}шт - {order[2][1][0]} ₴
┗ За Всё время: {order[3][1][1]}шт - {order[2][1][0]} ₴

🎁 Товары
┣ Товаров: {len(goods)}шт
┗ Категорий: {len(categories)}шт
"""


def build_all_orders_msg(orders: Iterable[Order]) -> str:
    resp = []
    for order in orders:
        readable_status = order_status.get(order.status)
        resp.append(
            f"Id - `{order.id}`\nСтатус - *{readable_status}*\nСтворенно - *{order.time_created}*\n"
        )
    return "\n".join(resp)
