import discord
from utils.tictactoe_game import TictactoeGame
from utils import funcs
from discord.ext import commands
from discord.ext import tasks


class Tictactoe(commands.Cog, name="Tic tac toe"):
    def __init__(self, client):
        self.client = client
        self.game_list = {}

    def check_channel_has_game(self, ctx):
        if self.game_list[ctx.channel.id]:
            return True

    def _get_game_from_list(self, channel_id: int):
        return self.game_list[channel_id]

    @commands.command(name="ttt_start", description="Start a tic tac toe game", usage="<@mention>")
    @commands.guild_only()
    async def start(self, ctx, target_player: discord.Member):
        player1 = ctx.message.author.id
        player2 = target_player.id
        if self.check_channel_has_game(ctx):
            await ctx.channel.send(embed=funcs.errorEmbed(None, "This channel still has a tic tac toe game going! "
                                                                "Please wait until it ends."))
        elif target_player.bot:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with bots."))
        elif player1 == player2:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with yourself..."))
        else:
            # let's do the messy stuff
            inital_game_board_embed = discord.Embed(
                color=discord.Color.blue(),
                title="{} vs {}".format(ctx.message.author.mention, target_player.mention),
            )
            self.game_list[ctx.channel.id] = TictactoeGame(player1, player2)  # add a instance of a game to game list
            inital_game_board_embed.description = str(self._get_game_from_list(ctx.channel.id))
            game_msg = await ctx.channel.send(embed=inital_game_board_embed)

    @commands.command(name="c")
    @commands.guild_only()
    async def clear(self, ctx):
        self.game_list = {}
        await ctx.channel.send("cleared")


def setup(client):
    client.add_cog(Tictactoe(client))
