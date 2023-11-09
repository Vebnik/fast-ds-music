import logging
from logging import Logger
from discord.ext.commands import Cog
from discord import Game, Status
from discord.ext.tasks import loop

from src.player.store import LavaStore


class Service(Cog):
    logger: Logger

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

        # tasks
        self.update_presence.start()

    # tasks
    @loop(seconds=30.0)
    async def update_presence(self):
        self.logger.info('Task - update_now_playing')

        try:
            players = LavaStore.node.players
            await self.bot.change_presence(
                activity=Game(name=f'🎵 on {len(players)} servers 🖥️'),
                status=Status.online if len(players) else Status.idle
            )
        except Exception as ex:
            self.logger.critical(ex)

    def cog_unload(self):
        self.update_presence.cancel()
