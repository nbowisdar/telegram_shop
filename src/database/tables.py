from peewee import Model, CharField, IntegerField, FloatField, SqliteDatabase, \
    ForeignKeyField, BooleanField
from setup import BASE_DIR
import os

db = SqliteDatabase(os.path.join(BASE_DIR, "app.db"))


class BaseModel(Model):
    class Meta:
        database = db


class Account(BaseModel):
    name = CharField()
    price = FloatField()


class Order(BaseModel):
    user_id = IntegerField()
    city = CharField()
    selfie = CharField()  # we will be store a file_id from tg
    sex = CharField()
    car = CharField(null=True)
    with_discount = BooleanField(default=False)
    note = CharField(null=True)
    account = ForeignKeyField(Account, backref="orders")


class PromoCode(BaseModel):
    name = CharField(unique=True)
    count_of_use = IntegerField(default=0)


def create_table():
    tables = [Account, Order, PromoCode]
    db.create_tables(tables)


if __name__ == '__main__':
    create_table()