import asyncio
import time

import discord
import httpx
from discord.ext import commands

from utils import funcs
from utils.emotes import emotes


class Utility(commands.Cog, name="Utility"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="urban", description="Urban Dictionary, but in Discord.", usage="<term>")
    @commands.cooldown(1, 5, commands.BucketType.default)
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
            await ctx.channel.send(embed=urban_embed)
            # TODO: add reaction menu

    @commands.command(name="wpm", description="Test your typing speed.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wpm(self, ctx):
        await ctx.message.add_reaction(emotes["loading"])
        async with httpx.AsyncClient() as client:
            res = await client.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
            full_extract = res.json()["extract"].split()[:49]
            extract = " ".join(full_extract)
        await ctx.send(content=extract.replace(" ", " ឵឵឵"))
        await ctx.message.clear_reaction(emotes["loading"])
        start_time = time.time()
        try:
            msg = await self.client.wait_for("message", timeout=120.0, check=lambda
                x: x.channel.id == ctx.channel.id and x.author.id == ctx.author.id)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Times out! Type faster next time.")
        else:
            input_text = msg.content
            if "឵឵឵" not in input_text:
                end_time = time.time()
                delta_time = end_time - start_time
                if (len(extract) * 0.2) > len(input_text):
                    await ctx.send(embed=funcs.errorEmbed(None, "You have made too many errors!"))
                    return
                count = 0
                for i, c in enumerate(extract):
                    if input_text[i] == c:
                        count += 1
                accuracy = round(count / len(extract) * 100, 2)
                wpm = round(len(input_text) * 60 / (5 * delta_time), 2)

                await ctx.send("**WPM:** {}\n"
                               "**Accuracy: ** {}%".format(wpm, accuracy))


def setup(client):
    client.add_cog(Utility(client))
