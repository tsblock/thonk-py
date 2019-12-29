import discord
import time
from utils import funcs
from utils.emotes import emotes
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping", description="Shows latency of the bot, also for checking if the bot is responding")
    async def ping(self, ctx):
        previous_time = int(round(time.time() * 1000))
        msg = await ctx.channel.send(emotes["thonkspin"])
        current_time = int(round(time.time() * 1000))
        delta = current_time - previous_time
        await msg.edit(content="{} `{}ms`".format(emotes["thonk"], delta))

    @commands.command(name="help", description="Shows a list of command")
    async def help(self, ctx, *cmd):
        if not cmd:  # no command specified
            listEmbed = discord.Embed(
                color=discord.Color.from_rgb(255, 255, 0)
            )
            listEmbed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
            for cogs in self.client.cogs:  # loop through each category
                if cogs == "Cleverbot": continue
                cmd_list = ""
                for cmd_name in self.client.get_cog(cogs).get_commands():
                    cmd_list += "`{}`\n".format(cmd_name)
                listEmbed.add_field(name=cogs, value=cmd_list)
            await ctx.channel.send(embed=listEmbed)
        else:
            if self.client.get_command(cmd[0]) is not None:
                cmd_object = self.client.get_command(cmd[0])
                name = cmd_object.name
                description = cmd_object.description
                usage = cmd_object.usage
                aliases = cmd_object.aliases
                cmdEmbed = discord.Embed(
                    color=discord.Color.from_rgb(255, 255, 0),
                    title=name
                )
                cmdEmbed.add_field(name="Description", value="```{}```".format(description))
                if usage is not None:
                    cmdEmbed.add_field(name="Usage", value="```t.{} {}```".format(name, usage))
                if len(aliases) != 0:
                    alias_text = ""
                    for alias in aliases:
                        alias_text += alias + ", "
                    cmdEmbed.add_field(name="Aliases", value="```{}```".format(alias_text))
                await ctx.channel.send(embed=cmdEmbed)

            else:
                error_embed = funcs.errorEmbed(None, "Command doesn't exist")
                await ctx.channel.send(embed=error_embed)

    @commands.command(name="invite", description="Shows the invite of this bot")
    async def invite(self, ctx):
        invite_embed = discord.Embed(
            description="[Click here!](https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=473196598&scope=bot)".format(self.client.user.id),
            color=discord.Color.from_rgb(255, 255, 0)
        )
        await ctx.channel.send(embed=invite_embed)


def setup(client):
    client.add_cog(General(client))
