from src.schemas import Period


def build_all_new_users_stat_msg(data: list[tuple[Period: int]]) -> str:
    return f"""
📊 Уся статистика:

    🔰 За добу - *{data[0][1]}*
    ⌚️ За неділю - *{data[1][1]}*
    🗓 За місяць - *{data[2][1]}*
    🌎 Юзерів загалом - *{data[3][1]}*
    """
