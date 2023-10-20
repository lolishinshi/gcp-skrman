from peewee import AutoField, CharField, Model

from ..db import db


class Sticker(Model):
    id = AutoField()
    file_id = CharField(max_length=128)
    file_unique_id = CharField(max_length=32, unique=True)
    file_type = CharField(max_length=16)

    class Meta:
        database = db
