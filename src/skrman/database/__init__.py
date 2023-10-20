from peewee import Database

from .db import db
from .models import Description, Sticker


def init(database: Database):
    database.create_tables([Sticker, Description])


init(db)
