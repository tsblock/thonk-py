from discord.ext import commands


class SixteenCraft(commands.Cog, name="16craft"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == "597028739616079893" and ctx.channel.id == "612962167284695040" and ctx.message.content == "**Server has stopped.** :octagonal_sign:":
            await self.client.get_channel("698924656253599765").send(
                "<@161973479858503680> server down fdskjflkdsfjdslkfdsk;l")


def setup(client):
    client.add_cog(SixteenCraft(client))
