from discord.ext import commands

import config
from utils import funcs


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # this is a dumb idea please don't do this
            # for some reason self.client.owner_id returns None and i have no idea why
            if ctx.author.id in config.cooldown_whitelist:
                ctx.command.reset_cooldown(ctx)
                return await self.client.process_commands(ctx.message)
            await ctx.channel.send(
                embed=funcs.error_embed("Hey! Calm down.",
                                        "Try again in `{}` seconds".format(round(error.retry_after, 2))))
        elif isinstance(error, commands.NotOwner):
            await ctx.channel.send(
                embed=funcs.error_embed("Insufficient permission", "Only bot owner can use this command."))
        elif isinstance(error, commands.UserInputError):
            await ctx.send(embed=funcs.error_embed("Invalid arguments!",
                                                   "Correct usage: `{}{} {}`".format(self.client.command_prefix,
                                                                                     ctx.command.name,
                                                                                     ctx.command.usage)))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(embed=funcs.error_embed(None,
                                                   "You can not use this command in private message."))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=funcs.error_embed("Insufficient permission",
                                                   "Permission(s) required: `{}`".format(
                                                       ", ".join(error.missing_perms))))


def setup(client):
    client.add_cog(ErrorHandler(client))
