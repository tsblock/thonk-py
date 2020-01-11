import discord
from discord.ext import commands

from database import economy
from utils import funcs
from utils.emotes import emotes


class Economy(commands.Cog, name="Economy"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="balance", description="Shows your balance", usage="[@mention]", aliases=["bal", "b"])
    async def balance(self, ctx, *target_member: discord.Member):
        if not target_member:
            target_member = ctx.author
        else:
            target_member = target_member[0]
        target_document = economy.get(target_member.id)
        balance_embed = discord.Embed(
            title="💰 {}'s wallet".format(target_member.name),
            description="**$** {}".format(target_document.balance),
            color=discord.Color.green()
        )
        await ctx.send(embed=balance_embed)

    @commands.command(name="pay", description="Pay money to someone", usage="<@mention> <amount>")
    async def pay(self, ctx, target_member: discord.Member, amount: int):
        self_document = economy.get(ctx.author.id)
        target_document = economy.get(target_member.id)
        self_balance = self_document.balance
        target_balance = target_document.balance
        if self_balance < amount:
            await ctx.send(embed=funcs.errorEmbed(None, "You don't have enough money!"))
            return
        if ctx.author.id == target_member.id:
            await ctx.send(embed=funcs.errorEmbed(None, "You can't pay to yourself..."))
            return
        if amount <= 0:
            await ctx.send(embed=funcs.errorEmbed(None, "What are you doing?"))
            return
        economy.add(ctx.author.id, -amount)
        economy.add(target_member.id, amount)
        pay_embed = discord.Embed(
            title="{} Payment done!".format(emotes["tick"]),
            description="You have sent ${} to {}".format(str(amount), target_member.mention)
        )
        await ctx.send(embed=pay_embed)


def setup(client):
    client.add_cog(Economy(client))
