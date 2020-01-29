import os

import discord
from discord.ext import commands
from mongoengine import connect

import config

# connect to database
connect("thonk", host=config.mongodb_url)

prefix = "t."
if not config.production:
    prefix = "tb."

client = commands.Bot(command_prefix=prefix)
client.remove_command("help")


@client.event
async def on_ready():
    print("Ready!")
    presence = discord.Activity(name="for {}".format(client.command_prefix), type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=presence)


for file in os.listdir("./category"):
    if file.endswith(".py"):
        client.load_extension(f"category.{file[:-3]}")

for file in os.listdir("./mods"):
    if file.endswith(".py"):
        client.load_extension(f"mods.{file[:-3]}")

client.run(config.token)
