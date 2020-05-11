import asyncio
from typing import Dict, List

import discord
import youtube_dl
from discord.ext import commands

from utils import funcs

ytdl_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn'  # disable video
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)


# TODO: implement playlist import
class Music(commands.Cog, name="Music"):
    def __init__(self, client):
        self.client = client
        self.queue = Dict[int, List[QueueEntry]]

    @commands.command(name="play", usage="<youtube url> / <search term>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, term):
        if ctx.author.voice is None:
            await ctx.send(embed=funcs.errorEmbed(None, "Please connect to a voice channel."))
            return

    def check_url(self, url):
        pass


class QueueEntry():
    def __init__(self, url):
        self.url = url

        # get video info


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.length = data.get("duration")
        self.progress = 0

    @classmethod
    async def from_url(cls, url, *, event_loop=None, stream=False):
        event_loop = event_loop or asyncio.get_event_loop()
        data = await event_loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def setup(client):
    client.add_cog(Music(client))
