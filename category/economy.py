import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from database import economy
from utils import funcs
from utils.emotes import emotes


class Economy(commands.Cog, name="Economy"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="balance", description="Shows your balance", usage="[@mention]", aliases=["bal", "b"])
    @commands.cooldown(3, 10, commands.BucketType.user)
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
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def pay(self, ctx, target_member: discord.Member, amount: int):
        self_document = economy.get(ctx.author.id)
        self_balance = self_document.balance
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
            description="You have sent ${} to {}".format(str(amount), target_member.mention),
            color=discord.Color.green()
        )
        await ctx.send(embed=pay_embed)

    @commands.command(name="daily", description="Claim daily reward")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def daily(self, ctx):
        self_document = economy.get(ctx.author.id)
        next_daily = self_document.next_daily
        present = datetime.utcnow()
        if next_daily is None or present > next_daily:
            economy.add(ctx.author.id, 1000)
            self_document.next_daily = present + timedelta(days=1)
            self_document.save()
            success_embed = discord.Embed(
                title="{} Daily reward has been claimed!".format(emotes["tick"]),
                description="**$** 1000 has been added to your wallet.",
                color=discord.Color.green()
            )
            await ctx.send(embed=success_embed)
        else:
            time_left = next_daily - present
            failed_embed = funcs.errorEmbed(None, funcs.format_timedelta(time_left, "Come back later in: {days} day, "
                                                                                    "{hours} hour, {minutes} minutes, "
                                                                                    "{seconds} seconds"))
            await ctx.send(embed=failed_embed)

    @commands.command(name="gamble", description="Pure gambling lol, 30% chance of winning.")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def gamble(self, ctx, amount: int):
        self_document = economy.get(ctx.author.id)
        self_balance = self_document.balance
        if self_balance < amount:
            await ctx.send(embed=funcs.errorEmbed(None, "You don't have enough money!"))
            return
        if amount <= 0:
            await ctx.send(embed=funcs.errorEmbed(None, "What are you doing?"))
            return
        luck = random.randrange(0, 100)
        if luck >= 50:
            economy.add(ctx.author.id, -amount)
            current_amount = self_balance - amount
            lost_embed = discord.Embed(
                title="💸 You lost!",
                description="Better luck next time!\nYou now have: **$** {}".format(str(current_amount)),
                color=discord.Color.red()
            )
            await ctx.send(embed=lost_embed)
        else:
            economy.add(ctx.author.id, amount)
            current_amount = self_balance + amount
            won_embed = discord.Embed(
                title="🤑 You won!",
                description="You now have: **$** {}".format(str(current_amount)),
                color=discord.Color.green()
            )
            await ctx.send(embed=won_embed)

    @commands.command(name="rob", description="Rob someone, a quick way to earn money, but high chance of being "
                                              "caught, good luck!", usage="<@mention/username> <amount>")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, target_member: discord.Member, amount: int):
        self_document = economy.get(ctx.author.id)
        self_balance = self_document.balance
        target_document = economy.get(target_member.id)
        target_balance = target_document.balance
        if self_balance < amount:
            await ctx.send(embed=funcs.errorEmbed(None, "You don't have enough money!"))
            return
        if amount <= 0:
            await ctx.send(embed=funcs.errorEmbed(None, "What are you doing?"))
            return
        if target_balance < amount:
            await ctx.send(embed=funcs.errorEmbed(None, "The user you tried to rob does not have enough money!"))
            return
        if ctx.author.id == target_member.id:
            await ctx.send(embed=funcs.errorEmbed(None, "I would love to see how you rob yourself."))
            return
        luck = random.randrange(1, 100)
        if luck <= 30:  # rob success!
            economy.add(ctx.author.id, amount)
            economy.add(target_member.id, -amount)
            success_embed = discord.Embed(
                title="😎 Here comes the money!",
                description="You have robbed {}\nYou now have **$** {}".format(target_member.mention,
                                                                               self_balance + amount),
                color=discord.Color.green()
            )
            await ctx.send(embed=success_embed)
            await target_member.send(
                "{} has robbed you, you now have **$** {}".format(ctx.author.name, target_balance - amount))
        else:
            penalty_amount = amount * 2
            if penalty_amount > self_balance:
                penalty_amount = self_balance
            economy.add(ctx.author.id, -penalty_amount)
            failed_embed = discord.Embed(
                title="🚔🚨🚔🚨 You just get caught!",
                description="You are too bad to rob someone lmaoamoamlamoaml\nYou now have **$** {}".format(
                    self_balance - penalty_amount),
                color=discord.Color.red()
            )
            await ctx.send(embed=failed_embed)


def setup(client):
    client.add_cog(Economy(client))
