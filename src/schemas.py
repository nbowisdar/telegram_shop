# from dataclasses import dataclass
import decimal
from datetime import datetime
from pydantic import BaseModel
from src.database.tables import Order


class AddressModel(BaseModel):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user: int


class GoodsModel(BaseModel):
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str


class UserModel(BaseModel):
    user_id: int
    orders: list["OrderModel"]
    address: AddressModel | None


class OrderModel(BaseModel):
    ordered_goods: GoodsModel
    amount: int
    user: UserModel
    with_discount: bool
    time_created: datetime | None = None
    note: str | None = None
