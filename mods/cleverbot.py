import re

import cleverbotfree.cbfree
from discord.ext import commands

cb = cleverbotfree.cbfree.Cleverbot()


class Cleverbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user in message.mentions and not message.content.startswith("t."):
            await message.channel.trigger_typing()
            if message.channel.id == 661589807901704222 and message.author.bot:
                msg = re.sub("<@!?" + str(self.client.user.id) + ">", "", message.content).strip()
                await message.channel.send(message.author.mention + " " + cb.single_exchange(msg))
            elif message.channel.id != 661589807901704222 and not message.author.bot:
                msg = re.sub("<@!?" + str(self.client.user.id) + ">", "", message.content).strip()
                await message.channel.send(message.author.mention + " " + cb.single_exchange(msg))


def setup(client):
    client.add_cog(Cleverbot(client))