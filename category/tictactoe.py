import discord
from discord.ext import commands

from utils import funcs
from utils.tictactoe_game import TictactoeGame


class Tictactoe(commands.Cog, name="Tic tac toe"):
    def __init__(self, client):
        self.client = client
        self.game_list = {}

    def check_channel_has_game(self, ctx):
        if self.game_list[ctx.channel.id]:
            return True

    def _get_game_from_list(self, channel_id: int):
        return self.game_list[channel_id]

    @commands.command(name="ttt_start", description="Start a tic tac toe game", usage="<@mention>", aliases=["tstart"])
    @commands.guild_only()
    async def start(self, ctx, target_player: discord.Member):
        player1 = ctx.message.author.id
        player2 = target_player.id

        if target_player.bot:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with bots."))
        elif player1 == player2:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "You can't start a game with yourself..."))
        elif ctx.channel.id in self.game_list:
            await ctx.channel.send(embed=funcs.errorEmbed(None, "This channel still has a tic tac toe game going! "
                                                                "Please wait until it ends."))
        else:
            initial_game_board_embed = discord.Embed(
                color=discord.Color.blue(),
                title="{} vs {}".format(ctx.message.author.name, target_player.name),
            )
            self.game_list[ctx.channel.id] = TictactoeGame(player1, player2)  # add a instance of a game to game list
            initial_game_board_embed.description = str(self._get_game_from_list(ctx.channel.id))
            game_msg = await ctx.channel.send("{}'s turn".format(ctx.message.author.name),
                                              embed=initial_game_board_embed)
            for reactions in funcs.number_emojis():
                await game_msg.add_reaction(reactions)
            await game_msg.add_reaction("⛔")
            self.game_list[ctx.channel.id].msg_id = game_msg.id

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if message.channel.id in self.game_list:
            if reaction.emoji == "⛔":
                if user.id == self.game_list[message.channel.id].player1 or user.id == self.game_list[message.channel.id].player2:
                    self.game_list.pop(message.channel.id, None)
                    await message.delete()
                    await message.channel.send("Game cancelled!")
                else:
                    await reaction.remove(user)
            else:
                if self.game_list[message.channel.id].turn == user.id:
                    index = funcs.number_emojis().index(reaction.emoji)
                    if self.game_list[message.channel.id][index] == "🔲":
                        self.game_list[message.channel.id].place(index)
                        if self.game_list[message.channel.id].check_for_win():
                            await message.delete()
                            await message.channel.send("{} wins! Congratulations. :tada:".format(
                                self.client.get_user(self.game_list[message.channel.id].winner).mention))
                            self.game_list.pop(message.channel.id, None)
                        elif self.game_list[message.channel.id].check_for_draw():
                            await message.delete()
                            await message.channel.send("It's a draw!")
                            self.game_list.pop(message.channel.id, None)
                        else:
                            updated_game_board_embed = message.embeds[0]
                            updated_game_board_embed.description = str(self.game_list[message.channel.id])
                            await message.edit(
                                content="{}'s turn".format(
                                    self.client.get_user(self.game_list[message.channel.id].turn).name),
                                embed=updated_game_board_embed)
                            await reaction.remove(user)
                    else:
                        await reaction.remove(user)
                elif user.id != self.client.user.id:
                    await reaction.remove(user)

def setup(client):
    client.add_cog(Tictactoe(client))
