import discord
from discord.ext import commands


class Connect4(commands.Cog, name="Connect 4"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="c4_start", description="Start a connect 4 game", usage="<@mention>", aliases=["cstart"])
    async def c4_start(self, ctx, target_player: discord.Member):
        pass


def setup(client):
    client.add_cog(Connect4(client))
