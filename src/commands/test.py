import logging
from logging import (
    Logger,
)
from discord.ext.commands import (
    Cog
)
from discord import (
    app_commands, Interaction, WebhookMessage
)
from src.player.store import (
    LavaStore,
)

from src.utils.embeds import (
    PlayEmbeds, ServiceEmbeds,
)


class Test(Cog):
    logger: Logger

    def __init__(self, bot):
        from main import MyClient

        self.bot: MyClient = bot
        self.logger = logging.getLogger('discord')

    @app_commands.command(name='test', description='A test command')
    async def test(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            if interaction.user.id != 324889109355298829:
                raise Exception('Ну ведь написано что тестовая команда, не тыкай её')

            tracks = await LavaStore.node.fetch_tracks('Kenshi Scorching Wind', search_type='ytsearch')

            mag: WebhookMessage = await interaction.followup.send(embed=PlayEmbeds.on_play(tracks[0]), wait=False)

            await interaction.followup.edit_message(mag.id, embed=PlayEmbeds.on_play(tracks[0]))

        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

# from collections import Counter
