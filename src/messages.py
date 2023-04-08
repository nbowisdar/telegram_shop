from aiogram.types import Message

from src.schemas import AddressModel, GoodsModel

'''
class GoodsModel(Base):
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str
'''


def build_goods_full_msg(goods: GoodsModel):
    return f"Назва - _{goods.name}_\n" \
           f"Опис - _{goods.desc}_\n" \
           f"Категорія - _{goods.category}_\n" \
           f"Ціна - *{float(goods.price)}* ₴\n" \
