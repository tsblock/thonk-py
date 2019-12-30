import os
from utils import funcs
import discord
from discord.ext import commands

import config

client = commands.Bot(command_prefix="t.")
client.remove_command("help")


@client.event
async def on_ready():
    print("Ready!")
    presence = discord.Game("t.")
    await client.change_presence(status=discord.Status.online, activity=presence)


for file in os.listdir("./category"):
    if file.endswith(".py"):
        client.load_extension(f"category.{file[:-3]}")

for file in os.listdir("./mods"):
    if file.endswith(".py"):
        client.load_extension(f"mods.{file[:-3]}")

client.run(config.token)
