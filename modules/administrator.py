import ast
import asyncio
import subprocess
import sys

import discord
from discord.ext import commands

import config
from database import economy
from utils import emotes, funcs


class Administrator(commands.Cog, name="Administrator"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="eval", description="execute python command")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        # credit: https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
        # thank you
        fn_name = "_eval_expr"

        code = code.strip("` ")

        code = "\n".join(f"    {i}" for i in code.splitlines())

        body = f"async def {fn_name}():\n{code}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'client': self.client,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'funcs': funcs,
            'emotes': emotes
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        success_embed = discord.Embed(
            title="{}".format(emotes.emotes["tick"]),
            color=discord.Color.green(),
            description="```xl\n{}```".format(result)
        )
        await ctx.channel.send(embed=success_embed)

    @commands.command(name="exec", description="Execute terminal command")
    @commands.is_owner()
    async def exec(self, ctx, *, cmd):
        await ctx.message.add_reaction(emotes.emotes["loading"])
        cmd_str_array = cmd.split(" ")
        try:
            output = subprocess.check_output(cmd_str_array)
            output = output.decode("unicode_escape")
        except subprocess.CalledProcessError as err:
            output = err.output.decode("unicode_escape")
            error_embed = discord.Embed(
                title="{}".format(emotes.emotes["cross"]),
                color=discord.Color.red(),
                description="```xl\n{}```".format(output)
            )
            await ctx.send(embed=error_embed)
        else:
            success_embed = discord.Embed(
                title="{}".format(emotes.emotes["tick"]),
                color=discord.Color.green(),
                description="```xl\n{}```".format(output)
            )
            await ctx.send(embed=success_embed)
        finally:
            await ctx.message.clear_reaction(emotes.emotes["loading"])

    @commands.command(name="say", description="SAY OSMETIHNG")
    @commands.is_owner()
    async def say(self, ctx, *arg):
        await ctx.channel.send(" ".join(arg))

    @commands.command(name="hack", description="hack into the nsa so you get FREE MOnEY!!!!")
    @commands.is_owner()
    async def hack(self, ctx, amount: int):
        member = ctx.author.id
        economy.add(member, amount)
        await ctx.send("omg you mad lad you hacked yourself some FREE MONEY!!!")

    @commands.command(name="reset_eco", description="proceed with caution lmaolmaomlmomalmaom")
    @commands.is_owner()
    async def reset_eco(self, ctx):
        if config.production:
            await ctx.send("why you are doing this in production")
        else:
            await ctx.send("are you ducking sure??? say yes (please :)) XDDDDDDDDDDDDD 😂😂😂😂😂😂😂😂😂😂😂")
            try:
                await self.client.wait_for("message", check=lambda m: m.content == "yes", timeout=5.0)
            except asyncio.TimeoutError:
                await ctx.send("lol pussy")
            else:
                for document in economy.EconomyDocument.objects:
                    document.delete()
                await ctx.send("Done! :)")

    @commands.command(name="restart", description="restart the bot")
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("✅❓")
        try:
            msg = await self.client.wait_for("message",
                                             check=lambda m: (m.author.id == ctx.author.id and m.content == "yes"),
                                             timeout=5.0)
        except asyncio.TimeoutError:
            await ctx.message.delete()
        else:
            await msg.add_reaction(str(emotes.emotes["loading"]))
            restart_indicator = open("restart_indicator", "w+")
            restart_indicator.write("{}:{}".format(msg.channel.id, msg.id))
            restart_indicator.close()
            sys.exit()


def setup(client):
    client.add_cog(Administrator(client))


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
