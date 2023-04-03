from datetime import datetime

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
    name = CharField(max_length=100)
    desc = TextField(null=True)
    price = DecimalField(max_digits=10, decimal_places=2)


class Address(BaseModel):
    full_name = CharField(max_length=100)
    mobile_number = CharField(max_length=15)
    city = CharField(max_length=50)
    post_number = IntegerField()
    user = ForeignKeyField(User, unique=True, backref="address")


class Order(BaseModel):
    time_created = DateTimeField(default=datetime.now)
    ordered_goods = ForeignKeyField(Goods, backref="orders")
    user = ForeignKeyField(User, backref="orders")
    with_discount = BooleanField(default=False)
    note = CharField(null=True)


class PromoCode(BaseModel):
    code = CharField(unique=True)
    count_of_use = IntegerField(default=0)


def create_table():
    tables = [Order, PromoCode, User, Address, Goods]
    db.create_tables(tables)


if __name__ == '__main__':
    create_table()