import math
from typing import (
    Any,
)
from discord import (
    Embed, Color
)
from mafic import (
    Track, Player,
)
from src.player.store import (
    PlayerStore,
)


class PlayEmbeds:
    @staticmethod
    def on_play(track: Track) -> Embed:
        embed = Embed(
            color=Color.brand_green(),
            title='Play',
            description=f'`title   ` [{track.title}]({track.uri})\n`duration` {track.length/1000/60} min.\n`author  ` ${track.author}'
        )

        return embed

    @staticmethod
    def on_pause(track: Track) -> Embed:
        embed = Embed(
            color=Color.brand_green(),
            title='Paused',
            description=f'`title   ` [{track.title}]({track.uri})'
        )

        return embed

    @staticmethod
    def on_resume(track: Track) -> Embed:
        embed = Embed(
            color=Color.brand_green(),
            title='Resumed',
            description=f'`title   ` [{track.title}]({track.uri})'
        )

        return embed

    @staticmethod
    def on_add(track: Track) -> Embed:
        embed = Embed(
            color=Color.brand_green(),
            title='Resumed',
            description=f'`title   ` [{track.title}]({track.uri})'
        )

        return embed

    @staticmethod
    def on_queue(tracks: list[Track]) -> Embed:
        description = [f'`{index+1}` [{track.title}]({track.uri})' for index, track in enumerate(tracks[:20])]

        embed = Embed(
            color=Color.brand_green(),
            title='Queue',
            description='\n'.join(description),
        )

        return embed

    @staticmethod
    def on_skip(track: Track) -> Embed:
        embed = Embed(
            color=Color.brand_green(),
            title='Skiped',
            description=f'`title   ` [{track.title}]({track.uri})',
        )
        return embed

    @staticmethod
    def on_now(player: Player, queue: list[Track]) -> Embed:
        track = player.current

        if not track:
            return Embed(color=Color.brand_green(), title='Now - Empty', description='')

        current_percent = int(player.position/(track.length/100))
        line_duration = '○'*45
        current_line_percent = math.ceil((len(line_duration)/100)*current_percent)
        current_line_duration = "❚"*current_line_percent
        current_line_duration = f'[{current_line_duration}{line_duration[current_line_percent:-1]}] ({current_percent} %)'
        track.title = track.title if len(track.title) < 59 else track.title[:59]

        current_track_description =\
            f"`title   ` [{track.title}]({track.uri})\n`duration` {'Live 🔴' if track.stream else round(track.length/1000/60, 2)}\n`author  ` ${track.author}"

        current_queue = "\n".join([f'`{index+1}` [{track.title}]({track.uri})' for index, track in enumerate(queue[:20])])

        embed = Embed(
            color=Color.brand_green(),
            title=f'Now - {"Paused" if player.paused else "Playing"}',
            description=current_track_description,
        )

        if not track.stream:
            embed.add_field(
                name='Progress',
                value=current_line_duration,
                inline=False,
            )

        embed.add_field(
            name='Queue',
            value=current_queue or 'Empty',
            inline=False,
        )

        return embed


class ServiceEmbeds:
    @staticmethod
    def on_error(data: Any) -> Embed:
        embed = Embed(
            color=Color.red(),
            title='Error',
            description=str(data)
        )

        return embed
