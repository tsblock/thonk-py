import asyncio
import time

import discord
import httpx
from discord.ext import commands
from googleapiclient.discovery import build

import config
from utils import funcs


class RandomStuff(commands.Cog, name="Random stuff"):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="cat", description="Shows a random cat")
    async def cat(self, ctx):
        res = await funcs.simple_get_request("https://some-random-api.ml/img/cat")
        file = await funcs.get_image_from_url(str(res["link"]))
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
        async with httpx.AsyncClient() as client:
            res = await client.get("http://api.urbandictionary.com/v0/define", params=params)
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

    @commands.command(name="wpm", description="Test your typing speed.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wpm(self, ctx):
        info_msg = await ctx.send("Getting an extract from Wikipedia...")
        await ctx.trigger_typing()
        async with httpx.AsyncClient() as client:
            res = await client.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
            full_extract = res.json()["extract"].split()[:49]
            extract = " ".join(full_extract)
        await info_msg.edit(content=extract.replace(" ", " ឵឵឵"))
        start_time = time.time()
        try:
            msg = await self.client.wait_for("message", timeout=120.0, check=lambda x: x.channel.id == ctx.channel.id and x.author.id == ctx.author.id)
        except asyncio.TimeoutError:
            await ctx.send("Times out! Type faster next time.")
        else:
            input_text = msg.content
            if "឵឵឵" in input_text:
                await ctx.send("Lol cheater.")
            else:
                end_time = time.time()
                delta_time = end_time - start_time
                count = 0
                for i, c in enumerate(extract):
                    if input_text[i] == c:
                        count += 1
                accuracy = round(count / len(extract) * 100, 2)
                wpm = round(len(input_text) * 60 / (5 * delta_time), 2)

                await ctx.send("**WPM:** {}\n"
                               "**Accuracy: ** {}%".format(wpm, accuracy))

    @commands.command(name="google", description="Perform Google search with the bot.", usage="<search term>")
    # @commands.cooldown(1, 10, commands.BucketType.channel)
    async def google(self, ctx, *, term):
        await ctx.trigger_typing()
        query_service = build("customsearch",
                              "v1",
                              developerKey=config.google_api_key)
        query_results = query_service.cse().list(q=term,
                                                 cx=config.google_cse_id, ).execute()
        results = query_results["items"]
        result_embed = discord.Embed(
            title="Google Search Results",
            color=discord.Color.blue()
        )
        for i in range(0, 5):
            result_embed.add_field(name="**{}. {}**".format(i + 1, results[i]["title"]), value=results[i]["link"],
                                   inline=False)
        await ctx.send(embed=result_embed)


def setup(client):
    client.add_cog(RandomStuff(client))
