# from dataclasses import dataclass
from typing import NamedTuple
import decimal
from datetime import datetime
from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        orm_mode = True


class AddressModel(Base):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user_id: int


class GoodsModel(Base):
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str


class AmountPrice(NamedTuple):
    amount: int
    price: decimal.Decimal


class OrderModel(Base):
    # ordered_goods: GoodsModel
    ordered_goods_id: int
    user_id: int
    total: decimal.Decimal
    type_payment: str
    discount: int = 0
    amount: int = None
    amount_disc: AmountPrice = None
    time_created: datetime | None = None
    note: str | None = None


# def from_dict_to_order_model(data: dict):



class UserModel(Base):
    user_id: int
    orders: list[OrderModel]
    address: AddressModel | None


class PromoCodeModel(Base):
    code: str
    max_use_left: int
    discount_percent: int


