import discord
from deep_translator import GoogleTranslator
from deep_translator import constants
from discord.ext import commands

from utils import funcs


class Translate(commands.Cog, name="Google Translate"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="translate",
                      description="Translate a text to other language"
                                  "\nSee https://gist.github.com/tsblock/6fe5977de3868a5b1fdb3d6e883bf228 \n"
                                  "for language code",
                      aliases=["tr"],
                      usage="<language to translate> <text>",
                      )
    @commands.cooldown(1, 10)
    async def translate(self, ctx, dest=None, *, msg=None):
        if dest not in constants.GOOGLE_CODES_TO_LANGUAGES.keys():
            await ctx.send(embed=funcs.error_embed(None, "Invalid language code! Please check "
                                                         "[this page](https://gist.github.com/tsblock/6fe5977de3868a5b1fdb3d6e883bf228)"
                                                         " for the list of valid language code."))
        else:
            await ctx.trigger_typing()
            res = GoogleTranslator(source="auto", target=dest).translate(text=msg)
            translate_embed = discord.Embed(
                color=discord.Color.green(),
                description="`{}`".format(res)
            )
            await ctx.channel.send(embed=translate_embed)

    @commands.command(name="literalchinese",
                      description="Literally translates Chinese text to English,"
                                  "\nprobably meaningless",
                      aliases=["lc"],
                      usage="<Chinese text lololl>")
    @commands.cooldown(1, 20)
    async def literal_chinese(self, ctx, *, msg):
        msg_list = list(msg)
        res = ""
        if len(res) > 50:
            await ctx.send(funcs.error_embed(None, "Inputs are too long!"))
            return
        await ctx.trigger_typing()
        translated_text_list = GoogleTranslator(source="zh-TW", target="en").translate_batch(msg_list)
        for translated_text in translated_text_list:
            if translated_text is None:
                translated_text = ""
            res += "{} ".format(translated_text)
        translate_embed = discord.Embed(
            color=discord.Color.green(),
            description="`{}`".format(res)
        )
        await ctx.channel.send(embed=translate_embed)


def setup(client):
    client.add_cog(Translate(client))
