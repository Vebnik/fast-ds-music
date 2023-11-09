import logging
from logging import Logger
from asyncio import sleep
from mafic import Player
from discord.ext.commands import Cog
from discord import app_commands, Interaction

from src.player.store import PlayerStore, LavaStore
from src.utils.embeds import PlayEmbeds, ServiceEmbeds


class Autocomplete:
    @classmethod
    async def play_autocomplete(cls, interaction: Interaction, current_source: str) -> list[app_commands.Choice[str]]:
        tracks = await LavaStore.node.fetch_tracks(current_source, search_type='ytsearch')

        PlayerStore.add_tracks(tracks, interaction.guild_id)

        return [
            app_commands.Choice(value=f'{index}', name=f'{item.title[:30]}')
            for index, item in [*enumerate(tracks[:10])]
        ]


class Test(Cog):
    logger: Logger

    def __init__(self, bot):
        from main import MyClient

        self.bot: MyClient = bot
        self.logger = logging.getLogger('discord')

    @app_commands.command(name='test', description='A test command')
    @app_commands.autocomplete(query=Autocomplete.play_autocomplete)
    async def test(self, interaction: Interaction, query: str) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            track = PlayerStore.get_tracks(interaction.guild_id)[int(query)]
            player = LavaStore.node.get_player(interaction.guild_id)

            PlayerStore.set_channel(interaction.channel, interaction.guild_id)

            if not player:
                current_channel = await interaction.client.fetch_channel(1084042267670614101)
                player = await current_channel.connect(cls=Player, self_deaf=True)

                await sleep(1)
                await player.play(track)
                await interaction.followup.send(embed=PlayEmbeds.on_play(track))
            else:
                await player.play(track)
                await interaction.followup.send(embed=PlayEmbeds.on_play(track))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

# from collections import Counter
