from src.database.queries import get_all_accounts


def show_accounts_price() -> str:
    msg = "Все доступные аккаунты\n"
    accounts = get_all_accounts()
    for acc in accounts:
        msg += f"{acc.name} - {acc.price} руб.\n"
    return msg
