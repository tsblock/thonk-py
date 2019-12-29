from discord.ext import commands
from utils import funcs
import aiohttp


class RandomImgTxt(commands.Cog, name="Random images and text"):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5,  commands.BucketType.default)
    @commands.command(name="cat", description="Shows a random cat")
    async def cat(self, ctx):
        res = await funcs.simple_get_request("http://aws.random.cat/meow")
        file = await funcs.get_image_from_url(str(res["file"]))
        await ctx.channel.send(file=file)

    @commands.cooldown(1, 5,  commands.BucketType.default)
    @commands.command(name="dog", description="Shows a random dog")
    async def dog(self, ctx):
        res = await funcs.simple_get_request("http://random.dog/woof.json")
        file = await funcs.get_image_from_url(str(res["url"]))
        await ctx.channel.send(file=file)

    @commands.cooldown(1, 5,  commands.BucketType.default)
    @commands.command(name="dadjoke", description="Shows a random dad joke", aliases=["pun", "puns"])
    async def dadjoke(self, ctx):
        header = {"Accept": "text/plain"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com/") as r:
                if r.status == 200:
                    res = await r.text()
                    await ctx.channel.send(res)



def setup(client):
    client.add_cog(RandomImgTxt(client))
