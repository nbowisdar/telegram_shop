# from dataclasses import dataclass
import enum
from typing import NamedTuple
import decimal
from datetime import datetime, timedelta
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
    id: int | None = None
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str
    is_in_box: bool


class AmountPrice(NamedTuple):
    amount: int
    price: decimal.Decimal


class OrderModel(Base):
    ordered_goods_id: int
    user_id: int
    total: decimal.Decimal
    type_payment: str
    discount: int = 0
    amount: int = None
    ordered_goods: GoodsModel | None = None
    ordered_goods_id: int | None = None
    amount_disc: AmountPrice = None
    time_created: datetime | None = None
    note: str | None = None


class Period(enum.Enum):
    day = datetime.now() - timedelta(days=1)
    week = datetime.now() - timedelta(days=7)
    month = datetime.now() - timedelta(days=30)
    year = datetime.now() - timedelta(days=360)
    all_time = datetime(year=2000, month=1, day=1)


per_by_name = {
    "week": Period.week,
    "day": Period.day,
    "month": Period.month,
    "year": Period.year,
    "all_time": Period.all_time,
}
# def get_period_by_name()

class UserModel(Base):
    user_id: int
    orders: list[OrderModel]
    address: AddressModel | None


class PromoCodeModel(Base):
    code: str
    max_use_left: int
    discount_percent: int


