from discord.ext import commands

from utils import funcs


class Music(commands.Cog, name="Music"):
    def __init__(self, client):
        self.client = client
        self.queue = {}

    @commands.command(name="play", usage="<youtube url>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, url: str):
        if not ctx.author.voice.channel:
            await ctx.send(embed=funcs.errorEmbed(None, "Please connect to a voice channel."))
            return


def setup(client):
    client.add_cog(Music(client))
