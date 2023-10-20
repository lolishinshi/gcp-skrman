from peewee import AutoField, BigIntegerField, CharField, DeferredForeignKey, Model
from playhouse.postgres_ext import TSVectorField

from ..db import db


class Description(Model):
    id = AutoField()
    user = BigIntegerField()
    sticker = DeferredForeignKey("Sticker")
    description = CharField(max_length=255)
    description_tsv = TSVectorField()

    class Meta:
        database = db
        indexes = ((("user", "sticker"), True),)
