from datetime import datetime
from config import categories
from peewee import Model, CharField, IntegerField, FloatField, SqliteDatabase, \
    ForeignKeyField, BooleanField, TextField, DecimalField, DateTimeField
from setup import BASE_DIR
import os
import decimal

db = SqliteDatabase(os.path.join(BASE_DIR, "app.db"))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)


class Goods(BaseModel):
    name = CharField(max_length=100, unique=True)
    desc = TextField(null=True)
    category = CharField(choices=categories)
    price = DecimalField(max_digits=10, decimal_places=2)
    photo = CharField(null=True)  # link to photo in tg


class Address(BaseModel):
    full_name = CharField(max_length=100)
    mobile_number = CharField(max_length=15)
    city = CharField(max_length=50)
    post_number = IntegerField()
    user = ForeignKeyField(User, unique=True, backref="address")


order_status = [("created", "🛒 Створенний"),
                ("wait_confirm", "⏳ Очікує підтвердження"),
                ("confirmed", "✅ Підтвердженно"),
                ("canceled", "🛑 Скасованно"),
                ("executed", "🎉 Виконанно")]


class Order(BaseModel):
    time_created = DateTimeField(default=datetime.now)
    ordered_goods = ForeignKeyField(Goods, backref="orders")
    amount = IntegerField()
    user = ForeignKeyField(User, backref="orders")
    discount = IntegerField(default=0)
    # total = DecimalField(max_digits=10, decimal_places=2)

    status = CharField(choices=order_status)
    note = CharField(null=True)


class PromoCode(BaseModel):
    code = CharField(unique=True)
    max_use = IntegerField(default=10000)
    discount_percent = IntegerField(default=10)


class UserCode(BaseModel):
    user = ForeignKeyField(User, backref="codes")
    code = ForeignKeyField(PromoCode, backref="users")


def create_table():
    tables = [Order, PromoCode, User, Address, Goods, UserCode]
    db.create_tables(tables)


if __name__ == '__main__':
    create_table()