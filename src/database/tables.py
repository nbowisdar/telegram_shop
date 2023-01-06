from peewee import Model, CharField, IntegerField, FloatField, SqliteDatabase, \
    ForeignKeyField, BooleanField
from setup import BASE_DIR
import os

db = SqliteDatabase(os.path.join(BASE_DIR, "app.db"))


class BaseModel(Model):
    class Meta:
        database = db


class Service(BaseModel):
    name = CharField()
    price = FloatField()


class Order(BaseModel):
    user_id = IntegerField()
    city = CharField()
    photo = CharField()  # we will be store a file_id from tg
    with_discount = BooleanField(default=False)
    note = CharField(null=True)
    service = ForeignKeyField(Service, backref="orders")


class PromoCode(BaseModel):
    name = CharField()
    count_of_use = IntegerField(default=0)


def create_table():
    tables = [Service, Order, PromoCode]
    db.create_tables(tables)


if __name__ == '__main__':
    create_table()