from src.db.models import PlayerData


class PlayerDataRepository:
    @classmethod
    def get(cls, guild_id: int | str) -> PlayerData | None:  # type: ignore
        try:
            return PlayerData.get(PlayerData.guild_id == guild_id)
        except Exception:
            return None

    @classmethod
    def create(cls, data: dict) -> None:  # type: ignore
        PlayerData.create(**data)

    @classmethod
    def create_or_update(cls, data: dict) -> None:
        try:
            player_data = PlayerData.get(PlayerData.guild_id == data.get('guild_id'))
        except Exception:
            player_data = None

        if player_data:
            for field in data:
                setattr(player_data, field, data[field])
            player_data.save()
        else:
            PlayerData.create(**data)
