from peewee import IntegrityError

from src.database.tables import db, Order, PromoCode, User, UserCode
import string
import random

from src.schemas import PromoCodeModel


def _generate_promo_code(num_char: int) -> str:
    code = ""
    symbl = string.ascii_letters + "0987654321"

    for i in range(num_char):
        code += random.choice(symbl)
    return code[0:4] + "_" + code[4:]


def generate_new_code(*, max_use_left=10000, discount_percent=10, num_char=8) -> PromoCodeModel:
    code = _generate_promo_code(num_char)
    while True:
        try:
            code = PromoCodeModel(code=code,
                                  max_use_left=max_use_left,
                                  discount_percent=discount_percent)
            PromoCode.create(**code.dict())
            print(code.code)
            return code
        except IntegrityError:
            pass


def apply_promo_code(code: str, user_id: int, use=False) -> PromoCodeModel:
    promo = PromoCode.get_or_none(PromoCode.code == code)
    if not promo:
        raise Exception("🛑 Такого промокода не існує!")
    elif promo.max_use_left <= 0:
        raise Exception("🛑 Цей промокод більше неможно використовувати!")
    user = User.get(user_id=user_id)
    used_codes = [code.code.code for code in user.codes]
    if code in used_codes:
        raise Exception("🛑 Ви вже використовували цей промокод!")
    if use:
        promo.max_use_left -= 1
        promo.save()
        UserCode.create(user=user, code=promo)
    return PromoCodeModel.from_orm(promo)
