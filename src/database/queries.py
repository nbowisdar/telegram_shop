from src.database.tables import db, Service, Order, PromoCode
import string
import random


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


def _get_promo():
    pass


def check_promo(name: str) -> bool:
    promo = PromoCode.get_or_none(PromoCode.name == name)
    if not promo:
        return False
    promo.count_of_use += 1
    promo.save()
    return True


if __name__ == '__main__':
    generate_new_code()