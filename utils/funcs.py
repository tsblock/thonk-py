from io import BytesIO

import discord
import httpx

import config
from utils.emotes import emotes


def error_embed(error_title, message):
    if error_title is None:
        error_title = "Error!"
    embed = discord.Embed(
        title="{} {}".format(emotes["cross"], error_title),
        color=discord.Color.red(),
        description=message
    )
    return embed


async def simple_get_request(url, params=None):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
    return r.json()


async def get_image_from_url(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code != 200:
            return None
        data = BytesIO(r.content)
        return discord.File(data, "placeholder." + url[-3:])


async def upload_text(text):
    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.paste.ee/v1/pastes", headers={
            "X-Auth-Token": config.pasteee_key,
            "Content-Type": "application/json"
        }, json={
            "sections":
                [
                    {
                        "contents": text
                    }
                ]
        })
        res = r.json()
        if not r.is_error:
            return res["link"]
        else:
            return "Upload failed!"


def number_emojis():
    return ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def format_timedelta(timedelta, time_str):
    d = {"days": timedelta.days}
    d["hours"], remain = divmod(timedelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(remain, 60)
    return time_str.format(**d)
