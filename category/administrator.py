import discord
from utils import emotes, funcs
from discord.ext import commands
import ast


class Administrator(commands.Cog, name="Administrator"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="eval", description="too lazy")
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
        try:
            result = (await eval(f"{fn_name}()", env))
            successEmbed = discord.Embed(
                title="{} Code executed successfully".format(emotes.emotes["tick"]),
                color=discord.Color.green(),
                description="```xl\n{}```".format(result)
            )
            await ctx.channel.send(embed=successEmbed)
        except Exception as err:
            failedEmbed = discord.Embed(
                title="{} Code failed successfully".format(emotes.emotes["cross"]),
                color=discord.Color.red(),
                description="```xl\n{}```".format(str(err))
            )

    @commands.command(name="say", description="SAY OSMETIHNG")
    @commands.is_owner()
    async def say(self, ctx, *arg):
        await ctx.channel.send(" ".join(arg))


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
