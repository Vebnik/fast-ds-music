import logging
from logging import Logger
from discord.ext.commands import Cog
from discord import app_commands, Interaction, Message
from mafic import Player
from discord.ext.tasks import loop

from src.player.store import LavaStore, PlayerStore
from src.utils.embeds import ServiceEmbeds, PlayEmbeds
from src.db.repository import PlayerDataRepository


class Autocomplete:
    @classmethod
    async def add_autocomplete(cls, interaction: Interaction, current_source: str) -> list[app_commands.Choice[str]]:

        tracks = await LavaStore.node.fetch_tracks(current_source, search_type='ytsearch')

        PlayerStore.add_tracks(tracks, interaction.guild_id)

        return [
            app_commands.Choice(value=f'{index}', name=f'{item.title[:30]}')
            for index, item in [*enumerate(tracks[:10])]
        ]


class PlayerControl(Cog):
    logger: Logger

    def __init__(self, bot):
        from main import MyClient

        self.bot: MyClient = bot
        self.logger = logging.getLogger('discord')

        # tasks
        self.update_now_playing.start()

    @app_commands.command(name='pause', description='A pause current player')
    async def pause(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)
            player = LavaStore.node.get_player(interaction.guild_id)

            await player.pause()
            await interaction.followup.send(embed=PlayEmbeds.on_pause(player.current))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='resume', description='A resume current player')
    async def resume(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)
            player = LavaStore.node.get_player(interaction.guild_id)

            await player.resume()
            await interaction.followup.send(embed=PlayEmbeds.on_resume(player.current))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='resume_session', description='A resume past player session')
    async def resume_session(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            current_channel = interaction.user.voice.channel
            player = await current_channel.connect(cls=Player, self_deaf=True)

            await interaction.followup.send(embed=PlayEmbeds.on_resume(player.current))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='add', description='Add new trak in queue')
    @app_commands.autocomplete(query=Autocomplete.add_autocomplete)
    async def add_to_queue(self, interaction: Interaction, query: str) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            track = PlayerStore.get_tracks(interaction.guild_id)[int(query)]
            PlayerStore.add_to_queue(track, interaction.guild_id)

            await interaction.followup.send(embed=PlayEmbeds.on_add(track))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='queue', description='Get queue')
    async def get_queue(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            tracks = PlayerStore.get_queue(interaction.guild_id)

            await interaction.followup.send(embed=PlayEmbeds.on_queue(tracks))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='skip', description='Skip to next track in queue')
    async def skip(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            player = LavaStore.node.get_player(interaction.guild_id)
            track = PlayerStore.get_queue(interaction.guild_id).pop(0)

            await player.play(track)

            await interaction.followup.send(embed=PlayEmbeds.on_skip(player.current))
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    @app_commands.command(name='now', description='Get current track info')
    async def now(self, interaction: Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True, thinking=False)

            player = LavaStore.node.get_player(interaction.guild_id)  # type: ignore
            queue = PlayerStore.get_queue(interaction.guild_id)  # type: ignore

            await interaction.followup.send(content='Sended')

            message: Message = await interaction.channel.send(embed=PlayEmbeds.on_now(player, queue))  # type: ignore

            PlayerStore.now_message_store[interaction.guild_id] = message  # type: ignore

            PlayerDataRepository.create_or_update({'last_now_channel': message.channel.id, 'message_id': message.id, 'guild_id': interaction.guild_id})
        except Exception as ex:
            self.logger.critical(ex)
            await interaction.followup.send(embed=ServiceEmbeds.on_error(ex))

    # tasks
    @loop(seconds=10)
    async def update_now_playing(self):
        self.logger.info('Task - update_now_playing')

        try:
            for player in LavaStore.node.players:
                now_msg = PlayerStore.now_message_store.get(player.guild.id)

                if not now_msg:
                    player_data = PlayerDataRepository.get(player.guild.id)

                    if not player_data:
                        return

                    now_msg = await self.bot.get_channel(player_data.last_now_channel).fetch_message(player_data.message_id) # type: ignore
                    PlayerStore.now_message_store[player.guild.id] = now_msg

                message = now_msg
                queue = PlayerStore.get_queue(player.guild.id)

                await message.edit(embed=PlayEmbeds.on_now(player, queue))
        except Exception as ex:
            self.logger.critical(ex)

    def cog_unload(self):
        self.update_now_playing.cancel()
