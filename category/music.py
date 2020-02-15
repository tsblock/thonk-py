from discord.ext import commands

from utils import funcs


class Music(commands.Cog, name="Music"):
    def __init__(self, client):
        self.client = client
        self.queue = {}

    @commands.command(name="play", usage="<youtube url> / <search term>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, term):
        if ctx.author.voice is None:
            await ctx.send(embed=funcs.errorEmbed(None, "Please connect to a voice channel."))
            return

    async def init(self, ctx, url):
        pass


class YTDLSource()


def setup(client):
    client.add_cog(Music(client))
