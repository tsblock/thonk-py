import time

import discord
from discord.ext import commands

from database import guild_settings
from utils import funcs
from utils.emotes import emotes


class General(commands.Cog, name="General"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping",
                      description="ping", aliases=["p"])
    async def ping(self, ctx):
        previous_time = int(round(time.time() * 1000))
        msg = await ctx.channel.send(emotes["thonkspin"])
        current_time = int(round(time.time() * 1000))
        delta = current_time - previous_time
        await msg.edit(content="{} `{}ms`".format(emotes["thonk"], delta))

    @commands.command(name="help", description="Shows a list of command", usage="[command]", aliases=["cmds", "h"])
    async def help(self, ctx, *cmd):
        if not cmd:  # no command specified
            list_embed = discord.Embed(
                color=discord.Color.from_rgb(255, 255, 0),
            )
            list_embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
            for cogs in self.client.cogs:  # loop through each modules
                if len(self.client.get_cog(cogs).get_commands()) == 0:
                    continue
                cmd_list = ""
                for cmd_name in self.client.get_cog(cogs).get_commands():
                    cmd_list += "`{}` ".format(cmd_name)
                list_embed.add_field(name=cogs, value=cmd_list, inline=False)
            await ctx.channel.send(embed=list_embed)
        else:
            if self.client.get_command(cmd[0]) is not None:
                cmd_object = self.client.get_command(cmd[0])
                name = cmd_object.name
                description = cmd_object.description
                usage = cmd_object.usage
                aliases = cmd_object.aliases
                cmd_embed = discord.Embed(
                    color=discord.Color.from_rgb(255, 255, 0),
                    title=name,
                    description="<> = Required, [] = Optional"
                )
                cmd_embed.add_field(name="Description", value="```{}```".format(description))
                if usage is not None:
                    cmd_embed.add_field(name="Usage", value="```t.{} {}```".format(name, usage))
                if len(aliases) != 0:
                    alias_text = ", ".join(aliases)
                    cmd_embed.add_field(name="Aliases", value="```{}```".format(alias_text))
                await ctx.channel.send(embed=cmd_embed)

            else:
                error_embed = funcs.error_embed(None, "Command doesn't exist")
                await ctx.channel.send(embed=error_embed)

    @commands.command(name="invite", description="Shows the invite of this bot")
    async def invite(self, ctx):
        invite_embed = discord.Embed(
            description="[Click here!](https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=473196598&scope=bot)".format(
                self.client.user.id),
            color=discord.Color.from_rgb(255, 255, 0)
        )
        await ctx.channel.send(embed=invite_embed)

    @commands.command(name="botinfo", description="Shows the information of the bot")
    async def botinfo(self, ctx):
        info_embed = discord.Embed(
            description="The worst bot ever made.",
            color=discord.Color.from_rgb(255, 255, 0)
        )
        info_embed.set_author(name="Thonk", icon_url=self.client.user.avatar_url)
        info_embed.add_field(name="Creator", value="`tsb#0534`")
        info_embed.add_field(name="Pycord version", value="`{}`".format(discord.__version__))
        info_embed.add_field(name="Creation date", value="`2018 August 17`")
        info_embed.add_field(name="Guilds", value="`{}`".format(str(len(self.client.guilds))))
        info_embed.add_field(name="Users", value="`{}`".format(str(len(self.client.users))))
        await ctx.send(embed=info_embed)
        pass

    @commands.command(name="toggle_msg", description="Toggle response messages")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def toggle_msg(self, ctx):
        guild_setting = guild_settings.get(ctx.guild.id)
        guild_setting.dumb_message = not guild_setting.dumb_message
        guild_setting.save()
        info_embed = discord.Embed(
            description="{} Response messages are now {}".format(emotes["tick"],
                                                                 "**on**" if guild_setting.dumb_message else "**off**"),
            color=discord.Color.green()
        )
        await ctx.send(embed=info_embed)


def setup(client):
    client.add_cog(General(client))
