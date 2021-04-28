import os

import discord
from discord.ext import commands
from mongoengine import connect

import config
from utils.emotes import emotes

# connect to database
connect("thonk", host=config.mongodb_url)

prefix = "t."
if not config.production:
    prefix = "tb."

# thanks discord
intents = discord.Intents.default()
intents.members = True  # for economy module
client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
client.remove_command("help")


@client.event
async def on_ready():
    print("Ready!")
    presence = discord.Activity(name="for {}help".format(client.command_prefix), type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=presence)
    await read_restart_indicator()


async def read_restart_indicator():
    if os.path.isfile("restart_indicator"):
        file = open("restart_indicator", "r")
        content = file.read()
        file.close()
        os.remove("restart_indicator")
        channel_id, msg_id = content.split(":")

        # react tick to message
        channel = await client.fetch_channel(channel_id)
        msg = await channel.fetch_message(msg_id)
        await msg.clear_reaction(emotes["loading"])
        await msg.add_reaction(emotes["tick"])

# load modules
for file in os.listdir("modules"):
    if file.endswith(".py"):
        client.load_extension(f"modules.{file[:-3]}")


client.run(config.token)
