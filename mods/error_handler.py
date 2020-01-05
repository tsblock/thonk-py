import discord
from discord.ext import commands
from utils import funcs


class error_handler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                embed=funcs.errorEmbed("Hey! Calm down.",
                                       "Try again in {} seconds".format(round(error.retry_after, 2))))
        elif isinstance(error, commands.NotOwner):
            await ctx.channel.send(
                embed=funcs.errorEmbed("Insufficient permission", "Only bot owner can use this command."))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=funcs.errorEmbed("Invalid arguments!",
                                                  "Correct usage: {}{} {}".format(self.client.command_prefix,
                                                                                  ctx.command.name,
                                                                                  ctx.command.usage)))


def setup(client):
    client.add_cog(error_handler(client))
