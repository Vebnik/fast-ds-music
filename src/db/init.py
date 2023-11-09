from peewee import SqliteDatabase


class DataBase:
    db = SqliteDatabase('main.db')

    @classmethod
    def init(cls) -> None:
        from src.db.models import PlayerData

        cls.db.create_tables([
            PlayerData,
        ])
