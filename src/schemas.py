# from dataclasses import dataclass
import decimal
from datetime import datetime
from pydantic import BaseModel
from src.database.tables import Order


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


class OrderModel(Base):
    ordered_goods: GoodsModel
    amount: int
    user_id: int
    discount: int = 0
    total: decimal.Decimal
    type_payment: str
    time_created: datetime | None = None
    note: str | None = None


# def from_dict_to_order_model(data: dict):



class UserModel(Base):
    user_id: int
    orders: list[OrderModel]
    address: AddressModel | None


class PromoCodeModel(Base):
    code: str
    max_use: int
    discount_percent: int


