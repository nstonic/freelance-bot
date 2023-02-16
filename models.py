import os
import datetime

from dotenv import load_dotenv
from peewee import *

load_dotenv()

db = SqliteDatabase(os.getenv('DATABASE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    telegram_id = IntegerField(primary_key=True)
    registered_at = DateTimeField(default=datetime.datetime.now)


class Freelancer(BaseModel):
    telegram_id = IntegerField(primary_key=True)
    access = BooleanField(default=True)
    registered_at = DateTimeField(default=datetime.datetime.now)


class Subscription(BaseModel):
    client = ForeignKeyField(Client, backref='subscriptions', on_delete='CASCADE')
    started_at = DateTimeField(default=datetime.datetime.now)
    duration = IntegerField(null=False)


class Ticket(BaseModel):
    client = ForeignKeyField(Client, backref='tickets', on_delete='CASCADE')
    title = CharField(max_length=100)
    text = TextField()
    rate = DecimalField()


class Order(BaseModel):
    ticket = ForeignKeyField(Ticket, backref='orders', on_delete='CASCADE')
    freelancer = ForeignKeyField(Freelancer, backref='orders', on_delete='CASCADE')
    estimate_time = CharField(max_length=100)
    started_at = DateTimeField(default=datetime.datetime.now)
    completed_at = DateTimeField(null=True)
    status = CharField(max_length=100, default='at_work') # posible_values: at_work, completed, cancelled


class Message(BaseModel):
    order = ForeignKeyField(Order, backref='messages', on_delete='CASCADE')
    telegram_id = CharField()
    text = TextField()
    sending_at = DateTimeField(default=datetime.datetime.now)


def create_tables():
    with db:
        db.create_tables([Client, Freelancer, Subscription, Ticket, Order, Message])
