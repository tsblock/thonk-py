from io import BytesIO

import discord
import httpx

from utils.emotes import emotes


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
    r = await httpx.get(url)
    if r.status_code == 200:
        return r.json()


async def get_image_from_url(url):
    r = await httpx.get(url)
    if r.status_code != 200:
        return None
    data = BytesIO(r.content)
    return discord.File(data, "aaa." + url[-3:])


def number_emojis():
    return ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def format_timedelta(timedelta, time_str):
    d = {"days": timedelta.days}
    d["hours"], remain = divmod(timedelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(remain, 60)
    return time_str.format(**d)
