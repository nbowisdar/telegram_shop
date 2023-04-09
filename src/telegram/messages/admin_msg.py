from src.database.tables import User
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
