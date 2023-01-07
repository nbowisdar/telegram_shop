from src.database.tables import db, Account, Order, PromoCode
import string
import random

from src.schemas import AccountModel


def _generate_promo_code(num_char: int) -> str:
    code = ""
    symbl = string.ascii_letters + "0987654321"

    for i in range(num_char):
        code += random.choice(symbl)
    return code


def generate_new_code(num_char=10) -> str:
    code = _generate_promo_code(num_char)
    PromoCode.create(name=code)
    return code


def check_promo(name: str, incr_amount=False) -> str | None:
    promo = PromoCode.get_or_none(PromoCode.name == name)
    if not promo:
        return
    if incr_amount:
        promo.count_of_use += 1
        promo.save()
    return name


def get_all_accounts() -> list[AccountModel]:
    return [
        AccountModel(name=acc.name, price=acc.price)
        for acc in Account.select()
    ]



if __name__ == '__main__':
    x = get_all_accounts()
    print(x)