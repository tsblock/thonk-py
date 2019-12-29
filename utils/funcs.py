import discord
from utils.emotes import emotes
import aiohttp
import io


def errorEmbed(error_title, message):
    if error_title is None:
        error_title = "Error!"
    embed = discord.Embed(
        title="{} {}".format(emotes["cross"], error_title),
        color=discord.Color.red(),
        description="`{}`".format(message)
    )
    return embed


async def simple_get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.json()


async def get_image_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if res.status != 200:
                return None
            data = io.BytesIO(await res.read())
            return discord.File(data, "abcd.png")
