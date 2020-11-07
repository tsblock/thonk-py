from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from game_models.connect4_game import Connect4Game
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

    @commands.command(name="c4_start", description="Start a connect 4 game", usage="<@mention>",
                      aliases=["cstart", "c4"])
    @commands.guild_only()
    async def c4_start(self, ctx, target_player: discord.Member):
        player1 = ctx.message.author.id
        player2 = target_player.id

        if target_player.bot:
            await ctx.channel.send(embed=funcs.error_embed(None, "You can't start a game with bots."))
        elif player1 == player2:
            await ctx.channel.send(embed=funcs.error_embed(None, "You can't start a game with yourself..."))
        elif ctx.channel.id in self.game_list:
            await ctx.channel.send(embed=funcs.error_embed(None, "This channel still has a Connect 4 game going! "
                                                                 "Please wait until it ends."))
        else:
            initial_game_board_embed = discord.Embed(
                color=discord.Color.blue(),
                title="{} vs {}\nReact with ⛔ to cancel the game".format(ctx.message.author.name, target_player.name),
            )
            self.game_list[ctx.channel.id] = Connect4Game(player1, player2)  # add a instance of a game to game list
            initial_game_board_embed.description = str(self._get_game_from_list(ctx.channel.id))
            game_msg = await ctx.channel.send("{}'s turn".format(ctx.message.author.name),
                                              embed=initial_game_board_embed)
            for num in range(7):
                await game_msg.add_reaction(funcs.number_emojis()[num])
            await game_msg.add_reaction("⛔")
            self.game_list[ctx.channel.id].last_react_time = datetime.utcnow()
            self.game_end_check_loop.start(game_msg)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel_id = message.channel.id
        numbers = funcs.number_emojis()[:-1]
        if user.bot:
            return
        if message.channel.id in self.game_list:
            if user.id == self.game_list[message.channel.id].player1 \
                    or user.id == self.game_list[message.channel.id].player2:
                if reaction.emoji == "⛔":
                    self.game_list.pop(channel_id, None)
                    await message.channel.send("Game cancelled!")
                else:
                    if reaction.emoji in numbers:
                        if self.game_list[channel_id].turn == user.id:
                            self.game_list[message.channel.id].last_react_time = datetime.utcnow()
                            index = numbers.index(reaction.emoji)
                            target_color = self.game_list[channel_id].getColorFromPlayer(user.id)
                            if self.game_list[channel_id].place(index, target_color):
                                if not self.game_list[channel_id].getWinner():
                                    if not self.game_list[channel_id].checkDraw():
                                        updated_game_board_embed = message.embeds[0]
                                        updated_game_board_embed.description = str(self.game_list[channel_id])
                                        await message.edit(content="{}'s turn".format(
                                            self.client.get_user(self.game_list[channel_id].turn).name),
                                            embed=updated_game_board_embed)
                                        await reaction.remove(user)
                                    else:
                                        await message.channel.send("It's a draw!")
                                        self.game_list.pop(channel_id, None)
                                else:
                                    await message.channel.send("{} won! Congratulations. :tada:".format(
                                        self.client.get_user(self.game_list[channel_id].getWinner()).mention))
                                    self.game_list.pop(channel_id, None)
                            else:
                                await reaction.remove(user)
                        else:
                            await reaction.remove(user)
                    else:
                        await reaction.remove(user)
            else:
                await reaction.remove(user)

    @tasks.loop(seconds=1.0)
    async def game_end_check_loop(self, message):
        if self.game_list[message.channel.id].winner is None:
            now = datetime.utcnow()
            if now - self.game_list[message.channel.id].last_react_time > timedelta(minutes=1.0):
                self.game_list.pop(message.channel.id, None)
                await message.channel.send("Game cancelled due to inactivity.")


def setup(client):
    client.add_cog(Connect4(client))
