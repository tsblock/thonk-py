import random

import discord
import httpx
from discord.ext import commands
from mcstatus import MinecraftServer

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

    @commands.command(name="16craft", description="Get status of 16craft", aliases=["16"])
    async def sixteen_craft(self, ctx):
        await ctx.channel.trigger_typing()
        server = MinecraftServer.lookup("16craft.serveminecraft.net:25565")
        try:
            status = server.status()
        except ConnectionError:
            error_embed = discord.Embed(
                title="16Craft Status",
                color=discord.Color.red(),
                description="**Server is offline.**"
            )
            error_embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/16craft.serveminecraft.net")
            await ctx.send(embed=error_embed)
        else:
            status_embed = discord.Embed(
                title="16Craft Status",
                color=discord.Color.green(),
            )
            status_embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/16craft.serveminecraft.net")
            status_embed.set_footer(text="Server IP: 16craft.serveminecraft.net | Server Reddit: r/16Craft")

            status_embed.add_field(name="Version", value=status.version.name.replace("Paper ", ""))
            status_embed.add_field(name="Player Count", value=status.players.online)
            players = []
            for player in status.players.sample:
                players.append(player.name)
            status_embed.add_field(name="Players", value=" ".join(players))
            await ctx.send(embed=status_embed)


def setup(client):
    client.add_cog(RandomStuff(client))
