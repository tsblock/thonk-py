from discord.ext import commands
from utils import funcs
import httpx
import discord


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

    @commands.cooldown(1, 10, commands.BucketType.default)
    @commands.command(name="lyric", description="Search a song's lyric")
    async def lyric(self, ctx, *, queried_song):
        params = {"title": queried_song}
        req = await httpx.get("https://some-random-api.ml/lyrics", params=params)
        res = req.json()
        # if res["error"] is not None:
        #     await ctx.channel.send(embed=funcs.errorEmbed(None, "Song doesn't exist."))
        title = res["title"]
        author = res["author"]
        lyrics = res["lyrics"][:2048]
        lyricEmbed = discord.Embed(
            color=discord.Color.green(),
            description=lyrics,
            title="{} - {}".format(author, title)
        )
        await ctx.channel.send(embed=lyricEmbed)



def setup(client):
    client.add_cog(RandomStuff(client))
