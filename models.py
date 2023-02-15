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
    access = BooleanField()
    registered_at = DateTimeField(default=datetime.datetime.now)


class Subscription(BaseModel):
    client = ForeignKeyField(Client, backref='subscriptions')
    started_at = DateTimeField(default=datetime.datetime.now)
    duration = IntegerField(null=False)


class Ticket(BaseModel):
    client = ForeignKeyField(Client, backref='tickets')  
    text = TextField()
    rate = DecimalField()


class Order(BaseModel):
    ticket = ForeignKeyField(Ticket)
    freelancer = ForeignKeyField(Freelancer, backref='orders')
    estimate_time = CharField(max_length=100)
    started_at = DateTimeField(default=datetime.datetime.now)
    completed_at = DateTimeField(null=True)
    status = CharField(max_length=100)


class Message(BaseModel):
    order = ForeignKeyField(Order, backref='messages')
    telegram_id = CharField()
    text = TextField()
    sending_at = DateTimeField(default=datetime.datetime.now)


def create_tables():
    with db:
        db.create_tables([Client, Freelancer, Subscription, Ticket, Order, Message])


if __name__ == '__main__':
    create_tables()
    print('Schema created')
