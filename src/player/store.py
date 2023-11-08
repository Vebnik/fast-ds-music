from mafic import (
    Track, Node, NodePool
)
from discord import (
    TextChannel
)
from discord import (
    Interaction, Message
)


class PlayerStore:
    channel_store: dict[str | int, TextChannel] = {}
    track_store: dict[str | int, list[Track]] = {}
    queue: dict[str | int, list[Track]] = {}
    now_message_store: dict[str | int, tuple[Message, Interaction]] = {}

    @classmethod
    def get_channel(cls, guild_id: str | int) -> TextChannel | None:
        return cls.channel_store.get(guild_id)

    @classmethod
    def set_channel(cls, channel: TextChannel, guild_id: str | int) -> None:
        cls.channel_store.update({guild_id: channel})

    @classmethod
    def add_tracks(cls, tracks: list[Track], guild_id: str | int) -> None:
        cls.track_store.update({guild_id: tracks})

    @classmethod
    def get_tracks(cls, guild_id: str | int) -> list[Track] | None:
        return cls.track_store.get(guild_id)

    @classmethod
    def add_to_queue(cls, track: Track, guild_id: str | int) -> None:
        if cls.queue.get(guild_id):
            cls.queue[guild_id].append(track)
        else:
            cls.queue.update({guild_id: [track]})

    @classmethod
    def get_queue(cls, guild_id: str | int) -> list[Track]:
        if cls.queue.get(guild_id):
            return cls.queue[guild_id]
        return []

    @classmethod
    def drop_data(cls, guild_id: str | int) -> None:
        del cls.channel_store[guild_id]
        del cls.track_store[guild_id]
        del cls.queue[guild_id]


class LavaStore:
    node: Node | None = None
    node_poll: NodePool | None = None
