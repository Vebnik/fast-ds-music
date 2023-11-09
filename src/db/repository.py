from src.db.models import PlayerData


class PlayerDataRepository:
    @classmethod
    def get(cls, guild_id: int | str) -> PlayerData | None:  # type: ignore
        return PlayerData.get(PlayerData.guild_id == guild_id)

    @classmethod
    def create(cls, data: dict) -> None:  # type: ignore
        PlayerData.create(**data)

    @classmethod
    def create_or_update(cls, data: dict) -> None:
        player_data: PlayerData = PlayerData.get(PlayerData.guild_id == data.get('guild_id'))

        if player_data:
            for field in data:
                setattr(player_data, field, data[field])
            player_data.save()
        else:
            PlayerData.create(**data)
