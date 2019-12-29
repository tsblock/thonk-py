import os
from utils import funcs
import discord
from discord.ext import commands

import config

client = commands.Bot(command_prefix="t.")
client.remove_command("help")


for file in os.listdir("./category"):
    if file.endswith(".py"):
        client.load_extension(f"category.{file[:-3]}")


@client.event
async def on_ready():
    print("Ready!")
    presence = discord.Game("t.")
    await client.change_presence(status=discord.Status.online, activity=presence)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send(embed=funcs.errorEmbed("Hey! Calm down.", "Try again in {} seconds".format(round(error.retry_after))))

client.run(config.token)
