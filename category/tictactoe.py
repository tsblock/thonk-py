import discord
from discord.ext import commands


class tictactoe(commands.Cog, name="Tic tac toe"):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(tictactoe(client))
