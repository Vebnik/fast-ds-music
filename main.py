import logging
from logging import (
    Logger
)
from mafic import (
    NodePool, Node
)
from discord import (
    Intents,
)
from discord.ext.commands import (
    Bot,
)
from config import (
    TOKEN, LAVA_HOST, LAVA_PORT, LAVA_LABEL,
    LAVA_PASSWORD
)
from src.commands import cogs
from src.player.store import LavaStore
from src.db.init import DataBase


class MyClient(Bot):

    logger: Logger
    pool: NodePool
    node: Node

    async def on_ready(self) -> None:
        self.logger = logging.getLogger('discord')

        self.logger.info(f'Logged on as {self.user}')

        self.logger.info(f'Try to import db -> {DataBase.db}')
        DataBase.init()

        self.logger.info('Try to create lava node')
        await self.add_lava_node()

        self.logger.info('Try to load cogs')
        await self.load_cogs()

        sync = await self.tree.sync()
        self.logger.info(f'Sync commands -> {len(sync)}')

    async def load_cogs(self) -> None:
        for cog in cogs:
            try:
                await self.add_cog(cog(self))
                self.logger.info(f'Cog -> {cog.__name__} | Loaded')
            except Exception as ex:
                self.logger.info(f'Cog -> {cog.__name__} | Error: {ex}')

    async def add_lava_node(self):
        try:
            self.pool = NodePool(self)
            self.node = await self.pool.create_node(
                host=LAVA_HOST, port=LAVA_PORT,
                label=LAVA_LABEL, password=LAVA_PASSWORD,
                secure=False
            )

            LavaStore.node = self.node
            LavaStore.node_poll = self.pool

        except Exception as ex:
            self.logger.critical(ex)


if __name__ == '__main__':
    intents = Intents.default()
    intents.message_content = True
    client = MyClient('$', intents=intents)
    client.run(TOKEN)
