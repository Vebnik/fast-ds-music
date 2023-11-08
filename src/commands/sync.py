from discord.ext.commands import (
    Cog,
)
from discord import (
    app_commands, Interaction,
)


class Sync(Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='sync', description='For manual sync slash command')
    @app_commands.default_permissions()
    async def play(self, interaction: Interaction, guild: int | None = None) -> None:
        print(interaction, guild)
