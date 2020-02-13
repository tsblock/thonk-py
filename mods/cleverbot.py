import re

import httpx
from discord.ext import commands

import config


class Cleverbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user in message.mentions and not message.content.startswith("t."):
            await message.channel.trigger_typing()
            msg = re.sub("<@!?" + str(self.client.user.id) + ">", "", message.content).strip()
            params = {'botid': 'b0dafd24ee35a477', 'custid': message.author.id, 'input': msg or 'Hello'}
            async with httpx.AsyncClient() as client:
                res = await client.get("https://www.pandorabots.com/pandora/talk-xml", params=params)
                text = res.text
                text = text[text.find('<that>') + 6:text.rfind('</that>')]
                text = text.replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;',
                                                                                                     '&').replace(
                    '<br>', ' ')
            await message.channel.send("{}, {}".format(message.author.mention, text))


@commands.Cog.listener()
async def on_ready(self):
    if config.production:
        await self.client.get_channel(661589807901704222).send("<@659739607365320725> i hate you so much")


def setup(client):
    client.add_cog(Cleverbot(client))
