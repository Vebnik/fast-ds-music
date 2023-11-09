import datetime
from peewee import Model
import peewee as pw

from src.db.init import DataBase


class BaseModel(Model):
    id = pw.AutoField(primary_key=True)
    created = pw.DateTimeField(default=datetime.datetime.now())
    modified = pw.DateTimeField(null=True)

    class Meta:
        database = DataBase.db


class PlayerData(BaseModel):
    last_now_channel = pw.BigIntegerField()
    guild_id = pw.BigIntegerField()
    message_id = pw.BigIntegerField()
