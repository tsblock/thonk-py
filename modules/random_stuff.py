import random

import httpx
from discord.ext import commands

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
        async with httpx.AsyncClient as client:
            r = await client.get("https://icanhazdadjoke.com", headers=header)
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

    @commands.command(name="8ball", description="Ask 8ball something", aliases=["8b"], usage="<question>")
    async def eight_ball(self, ctx, *, placeholder):
        answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.",
                   "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        answer = random.choice(answers)
        await ctx.send("🎱: `{}`".format(answer))


def setup(client):
    client.add_cog(RandomStuff(client))
