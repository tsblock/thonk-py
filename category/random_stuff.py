import asyncio
from datetime import datetime

import discord
import httpx
from discord.ext import commands

from utils import funcs


class RandomStuff(commands.Cog, name="Random stuff"):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="cat", description="Shows a random cat")
    async def cat(self, ctx):
        res = await funcs.simple_get_request("http://aws.random.cat/meow")
        file = await funcs.get_image_from_url(str(res["file"]))
        await ctx.channel.send(file=file)

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="dog", description="Shows a random dog")
    async def dog(self, ctx):
        res = await funcs.simple_get_request("http://random.dog/woof.json")
        file = await funcs.get_image_from_url(str(res["url"]))
        await ctx.channel.send(file=file)

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="dadjoke", description="Shows a random dad joke", aliases=["pun", "puns"])
    async def dadjoke(self, ctx):
        header = {"Accept": "text/plain"}
        r = await httpx.get("https://icanhazdadjoke.com", headers=header)
        if r.status_code == 200:
            await ctx.channel.send(r.text)

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="catfact", description="Shows a random cat fact")
    async def catfact(self, ctx):
        res = await funcs.simple_get_request("https://some-random-api.ml/facts/cat")
        await ctx.channel.send(str(res["fact"]))

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="trumpquote", description="SHOWS A RANDOM TRUMP QUOTE!!!!1111111111")
    async def trumpquote(self, ctx):
        res = await funcs.simple_get_request("https://api.tronalddump.io/random/quote")
        await ctx.channel.send(str(res["value"]))

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="birb", description="Shows a random bird")
    async def birb(self, ctx):
        res = await funcs.simple_get_request("https://some-random-api.ml/img/birb")
        file = await funcs.get_image_from_url(str(res["link"]))
        await ctx.channel.send(file=file)

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="urban", description="Urban Dictionary, but in Discord.", usage="<term>")
    async def urban(self, ctx, *, term):
        params = {"term": term}
        res = await httpx.get("https://api.urbandictionary.com/v0/define", params=params)
        data = res.json()["list"]
        await ctx.trigger_typing()
        if len(data) == 0:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "Term does not exist."))
        else:
            urban_embed = discord.Embed(
                color=discord.Color.from_rgb(255, 255, 0),
                title=term
            )
            definition = data[0]["definition"].replace("[", "").replace("]", "")
            example = data[0]["example"].replace("[", "").replace("]", "")
            thumbs_up = data[0]["thumbs_up"]
            thumbs_down = data[0]["thumbs_down"]
            author = data[0]["author"]
            urban_embed.add_field(name="Definition", value=definition)
            if example:
                urban_embed.add_field(name="Example", value=example)
            urban_embed.set_footer(text="👍 {} | 👎 {} | By: {}".format(str(thumbs_up), str(thumbs_down), author))
            msg = await ctx.channel.send(embed=urban_embed)
            # await msg.add_reaction("◀")
            # await msg.add_reaction("▶")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="wpm", description="Test your typing speed.")
    async def wpm(self, ctx):
        return ctx.send("wip")
        info_msg = await ctx.send("Getting an extract from Wikipedia...")
        await ctx.trigger_typing()
        async with httpx.AsyncClient() as client:
            res = await client.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
            full_extract = res.json()["extract"].split()[:49]
            extract = " ".join(full_extract)
            extract.replace(" ", " ឵឵឵")  # prevent copy and pasting lolololo
        await info_msg.delete()
        await ctx.send(extract)
        await ctx.send("original string: " + " ".join(full_extract))
        start_time = datetime.utcnow()
        try:
            msg = await self.client.wait_for("message", timeout=120.0, check=lambda x: x.channel.id == ctx.channel.id)
        except asyncio.TimeoutError:
            await ctx.send("lol too slow")
        else:
            content = msg.content
            if "឵឵឵" in content:
                await ctx.send("wow cheater")
            else:
                pass

def setup(client):
    client.add_cog(RandomStuff(client))
