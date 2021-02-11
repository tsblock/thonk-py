import typing

import discord
import httpx
from discord.ext import commands

from utils import funcs

coingecko_api_base_url = "https://api.coingecko.com/api/v3/"


def get_ticker_to_coin_id():  # converts ticker to coingecko's id because their api are weird
    tickers = {}
    r = httpx.get(coingecko_api_base_url + "coins/list")
    coins_info = r.json()
    for coin_info in coins_info:
        coin_ticker = coin_info["symbol"]
        coin_id = coin_info["id"]
        tickers[coin_ticker] = coin_id
    return tickers


tickers = get_ticker_to_coin_id()


class CryptoCurrency(commands.Cog, name="Cryptocurrency"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="coin_price", description="Get the current price of a cryptocurrency.", aliases=["cp"],
                      usage="<coin ticker> [fiat currency]")
    async def coin_price(self, ctx, ticker: str, fiat_currency: typing.Optional[str] = "usd"):
        id = tickers.get(ticker.casefold(), None)
        fiat_currency = fiat_currency.casefold()
        if id:
            market_info = await funcs.simple_get_request(coingecko_api_base_url + "coins/markets",
                                                         params={"vs_currency": fiat_currency, "ids": id})
            market_info = market_info[0]
            if market_info.get("error", None):
                await ctx.send(embed=funcs.error_embed(None, "Invalid fiat currency"))
                return
            fiat_currency = fiat_currency.upper()
            name = market_info["name"]
            thumbnail = market_info["image"]
            current_price = str(market_info["current_price"]) + " " + fiat_currency
            market_cap = str(market_info["market_cap"]) + " " + fiat_currency
            market_cap_rank = str(market_info["market_cap_rank"])
            circulating_supply = str(market_info["circulating_supply"])
            max_supply = str(market_info["max_supply"])
            ath = str(market_info["ath"]) + " " + fiat_currency
            atl = str(market_info["atl"]) + " " + fiat_currency
            price_change_percentage_24h = str(market_info["price_change_percentage_24h"]) + "%"
            color = bull_or_bear(price_change_percentage_24h)
            try:
                market_info_embed = discord.Embed(title=name, color=color)
                market_info_embed.set_thumbnail(url=thumbnail)
                market_info_embed.add_field(name="💵 Current Price", value=f"`{current_price}`")
                market_info_embed.add_field(name="🏅 Market Cap Rank", value=f"`{market_cap_rank}`")
                market_info_embed.add_field(name="💹 Market Cap", value=f"`{market_cap}`")
                market_info_embed.add_field(name="🔁 Circulating Supply", value=f"`{circulating_supply}`")
                market_info_embed.add_field(name="🚚 Maximum Supply", value=f"`{max_supply}`")
                market_info_embed.add_field(name="📈 All-time High", value=f"`{ath}`")
                market_info_embed.add_field(name="📊 Price Change (24h)", value=f"`{price_change_percentage_24h}`")
                await ctx.send(embed=market_info_embed)
            except Exception as e:
                await ctx.send("LOOOOOOOOOOOOOOOOOOOL")
                await ctx.send(e)
        else:
            await ctx.send(embed=funcs.error_embed("Invalid coin ticker!", "Be sure to use the ticker. (e.g. `btc`)"))


def bull_or_bear(percentage):
    if "-" in percentage:  # why would you do this
        return discord.Color.red()
    else:
        return discord.Color.green()


def setup(client):
    client.add_cog(CryptoCurrency(client))
