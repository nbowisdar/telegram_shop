from peewee import Model, CharField, IntegerField, SqliteDatabase

db = SqliteDatabase("app.db")


class BaseModel(Model):
    class Meta:
        database = db


class Foo(BaseModel):
    hello = CharField()
    World = CharField()