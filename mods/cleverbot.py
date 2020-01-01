from discord.ext import commands
import cleverbotfree.cbfree
import re

cb = cleverbotfree.cbfree.Cleverbot()


class Cleverbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user in message.mentions and not message.content.startswith("t."):
            if message.channel.id == 661589807901704222 and message.author.bot:
                async with message.channel.typing():
                    msg = re.sub("<@!?" + str(self.client.user.id) + ">", "", message.content).strip()
                    await message.channel.send(message.author.mention + " " + cb.single_exchange(msg))


def setup(client):
    client.add_cog(Cleverbot(client))
