import discord
from discord.ext import commands

from game_models.connect4game import Connect4Game
from utils import funcs


class Connect4(commands.Cog, name="Connect 4"):
    def __init__(self, client):
        self.client = client
        self.game_list = {}

    def check_channel_has_game(self, ctx):
        if self.game_list[ctx.channel.id]:
            return True

    def _get_game_from_list(self, channel_id: int):
        return self.game_list[channel_id]

    @commands.command(name="c4_start", description="Start a connect 4 game", usage="<@mention>", aliases=["cstart"])
    @commands.guild_only()
    async def c4_start(self, ctx, target_player: discord.Member):
        player1 = ctx.message.author.id
        player2 = target_player.id

        if target_player.bot:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with bots."))
        elif player1 == player2:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with yourself..."))
        elif ctx.channel.id in self.game_list:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "This channel still has a Connect 4 game going! "
                                                                "Please wait until it ends."))
        else:
            initial_game_board_embed = discord.Embed(
                color=discord.Color.blue(),
                title="{} vs {}".format(ctx.message.author.name, target_player.name),
            )
            self.game_list[ctx.channel.id] = Connect4Game(player1, player2)  # add a instance of a game to game list
            initial_game_board_embed.description = str(self._get_game_from_list(ctx.channel.id))
            game_msg = await ctx.channel.send("{}'s turn".format(ctx.message.author.name),
                                              embed=initial_game_board_embed)
            for num in range(7):
                await game_msg.add_reaction(funcs.number_emojis()[num])
            await game_msg.add_reaction("⛔")

    @commands.command(name="c")
    async def c(self, ctx):
        self.game_list[ctx.channel.id] = None
        await ctx.send("done ffs")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel_id = message.channel.id
        numbers = funcs.number_emojis()[:-3]
        if message.channel.id in self.game_list:
            if reaction.emoji == "⛔":
                if user.id == self.game_list[channel_id].player1 or user.id == self.game_list[channel_id].player2:
                    self.game_list.pop(channel_id, None)
                    await message.delete()
                    await message.channel.send("Game cancelled!")
                else:
                    await reaction.remove(user)
            else:
                pass


def setup(client):
    client.add_cog(Connect4(client))
