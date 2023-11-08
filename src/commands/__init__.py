from .play import Play
from .sync import Sync
from .player_control import PlayerControl
from .test import Test


cogs = [
    # music
    Play,
    PlayerControl,

    # service
    Sync,
    Test,
]
