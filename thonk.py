import os
from utils import funcs
import discord
from discord.ext import commands

import config

client = commands.Bot(command_prefix="tb.")
client.remove_command("help")


@client.event
async def on_ready():
    print("Ready!")
    presence = discord.Game(client.command_prefix)
    await client.change_presence(status=discord.Status.online, activity=presence)
    if config.production:
        await client.get_channel(661589807901704222).send("<@659739607365320725> i hate you so much")

for file in os.listdir("./category"):
    if file.endswith(".py"):
        client.load_extension(f"category.{file[:-3]}")

for file in os.listdir("./mods"):
    if file.endswith(".py"):
        client.load_extension(f"mods.{file[:-3]}")

client.run(config.token)
