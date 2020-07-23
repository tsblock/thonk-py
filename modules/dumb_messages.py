import discord
from discord.ext import commands

from database import guild_settings


class dumb_messages(commands.Cog, name="dumb messages"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        content = ctx.content
        if ctx.guild is None:
            return
        if content.casefold() == "f":
            guild_setting = guild_settings.get(ctx.guild.id)
            if guild_setting.dumb_message:
                f_file = open("assets/f.jpg", "rb")
                discord_file = discord.File(fp=f_file)
                await ctx.channel.send(file=discord_file)


def setup(client):
    client.add_cog(dumb_messages(client))
