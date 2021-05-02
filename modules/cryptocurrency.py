import io
import typing
from datetime import datetime

import discord
import httpx
import mplfinance as mpf
from discord.ext import commands
from pandas import DataFrame, DatetimeIndex

import config
from utils import funcs

coingecko_api_base_url = "https://api.coingecko.com/api/v3/"
coin360_heatmap_api_url = "https://coin360.com/api/share?width=1920&height=1080&path=/&search=getScreen%26zoom%3D%7B%22x%22%3A0%2C%22y%22%3A0%2C%22k%22%3A1%7D"
mempool_space_api_url = "https://mempool.space/api/v1/"
ethgasstation_api_url = "https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key={}".format(
    config.ethgasstation_key)


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

    @commands.cooldown(1, 5, commands.BucketType.default)
    @commands.command(name="coin_price", description="Get the current price of a cryptocurrency.", aliases=["cp"],
                      usage="<coin ticker> [to currency]")
    async def coin_price(self, ctx, ticker: str = "btc", fiat_currency: typing.Optional[str] = "usd"):
        id = tickers.get(ticker.casefold(), None)
        fiat_currency = fiat_currency.casefold()
        if id:
            await ctx.trigger_typing()
            market_info = await funcs.simple_get_request(coingecko_api_base_url + "coins/markets",
                                                         params={"vs_currency": fiat_currency, "ids": id,
                                                                 "price_change_percentage": "1h,24h,7d,1y"})
            market_info = market_info[0]  # the api returns an array so only get the first result
            if market_info.get("error", None):  # detect invalid vs_currency
                await ctx.send(embed=funcs.error_embed(None, "Invalid currency."))
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
            price_change_percentage_1h = str(round(market_info["price_change_percentage_1h_in_currency"], 4)) + "%"
            price_change_percentage_24h = str(round(market_info["price_change_percentage_24h_in_currency"], 4)) + "%"
            price_change_percentage_7d = str(round(market_info["price_change_percentage_7d_in_currency"], 4)) + "%"
            price_change_percentage_1y = str(round(market_info["price_change_percentage_1y_in_currency"], 4)) + "%"
            last_updated = market_info["last_updated"]
            color = bull_or_bear(price_change_percentage_24h)

            market_info_embed = discord.Embed(color=color)
            market_info_embed.set_author(name=name, icon_url=thumbnail)
            market_info_embed.add_field(name="💵 Current Price", value=f"`{current_price}`")
            market_info_embed.add_field(name="🏅 Market Cap Rank", value=f"`{market_cap_rank}`")
            market_info_embed.add_field(name="💹 Market Cap", value=f"`{market_cap}`")
            market_info_embed.add_field(name="🔁 Circulating Supply", value=f"`{circulating_supply}`")
            market_info_embed.add_field(name="🚚 Maximum Supply", value=f"`{max_supply}`")
            market_info_embed.add_field(name="📈 All-time High", value=f"`{ath}`")
            market_info_embed.add_field(name="📊 Price Change (1h)", value=f"`{price_change_percentage_1h}`")
            market_info_embed.add_field(name="📊 Price Change (24h)", value=f"`{price_change_percentage_24h}`")
            market_info_embed.add_field(name="📊 Price Change (7d)", value=f"`{price_change_percentage_7d}`")
            market_info_embed.add_field(name="📊 Price Change (1y)", value=f"`{price_change_percentage_1y}`")
            market_info_embed.set_footer(text="Data provided by CoinGecko", icon_url="https://i.imgur.com/7nzhHrl.png")
            market_info_embed.timestamp = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")

            await ctx.send(embed=market_info_embed)
        else:
            await ctx.send(embed=funcs.error_embed("Invalid coin ticker!", "Be sure to use the ticker. (e.g. `btc`)"))

    @commands.command(name="coin_chart", description="Get a cryptocurrency price chart",
                      usage="<coin ticker> [option 1, option 2, option 3...]\n"
                            "Available intervals: d, w, m, y\n"
                            "Available options: ma, line", aliases=["cc"])
    async def coinchart(self, ctx, ticker, *options):
        id = tickers.get(ticker.casefold(), None)
        days = "1"
        mav = None
        chart_type = "candle"
        for option in options:
            option = option.casefold()
            if option == "d":
                days = "1"
            elif option == "w":
                days = "7"
            elif option == "m":
                days = "30"
            elif option == "y":
                days = "365"
            elif option == "ma":
                mav = (3, 7, 25)
            elif option == "line":
                chart_type = "line"
        if id:
            await ctx.trigger_typing()
            ohlc_data = await funcs.simple_get_request(coingecko_api_base_url + "coins/{}/ohlc".format(id),
                                                       params={"vs_currency": "usd", "days": days})
            coin_info = await funcs.simple_get_request(coingecko_api_base_url + "coins/{}".format(id))
            df = DataFrame(
                [date[1:] for date in ohlc_data],
                index=DatetimeIndex([datetime.utcfromtimestamp(date[0] / 1000) for date in ohlc_data]),
                columns=["Open", "High", "Low", "Close"]
            )
            buffer = io.BytesIO()
            mc = mpf.make_marketcolors(base_mpf_style="binance", inherit=True)
            style = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=mc)
            # hacky hack hack
            if mav:
                mpf.plot(df, type=chart_type, style=style, ylabel="Price (USD)",
                         title="{}d Chart ({})".format(days, coin_info["name"]), mav=mav, savefig=buffer)
            else:
                mpf.plot(df, type=chart_type, style=style, ylabel="Price (USD)",
                         title="{}d Chart ({})".format(days, coin_info["name"]), savefig=buffer)
            buffer.seek(0)
            await ctx.send(file=discord.File(fp=buffer, filename="chart.png"))
        else:
            await ctx.send(embed=funcs.error_embed("Invalid coin ticker!", "Be sure to use the ticker. (e.g. `btc`)"))

    # doesnt work for now
    # @commands.cooldown(1, 30, commands.BucketType.default)
    # @commands.command(name="coin_price_heatmap", description="Shows the heatmap of cryptocurrencies prices.",
    #                   aliases=["cphmap", "cphm"])
    # async def coin_price_heatmap(self, ctx):
    #     try:
    #         await ctx.trigger_typing()
    #         res = await funcs.simple_get_request(coin360_heatmap_api_url)
    #         print(res)
    #         image_url = "https://coin360.com/shareimg/{}".format(res["url"])
    #         image = await funcs.get_image_from_url(image_url)
    #         await ctx.send(file=image)
    #     except Exception as e:
    #         print(e)

    @commands.command(name="btcfees", description="Shows the recommended fees for Bitcoin transactions", aliases=["bf"])
    async def btcfees(self, ctx):
        fees = await funcs.simple_get_request(mempool_space_api_url + "/fees/recommended")
        fees_embed = discord.Embed(title="Bitcoin transactions fees", color=0xf7931a)
        fees_embed.add_field(name="High priority (~10m)", value="`{} sats/vB`".format(fees["fastestFee"]))
        fees_embed.add_field(name="Medium priority (~3h)", value="`{} sats/vB`".format(fees["halfHourFee"]))
        fees_embed.add_field(name="Low priority (~1d)", value="`{} sats/vB`".format(fees["hourFee"]))
        fees_embed.add_field(name="Minimum", value="`{} sats/vB`".format(fees["minimumFee"]))
        await ctx.send(embed=fees_embed)

    @commands.command(name="ethgas", description="Shows the recommended gas fees for Ethereum transactions",
                      aliases=["eg"])
    async def ethgas(self, ctx):
        fees = await funcs.simple_get_request(ethgasstation_api_url)
        fees_embed = discord.Embed(title="Ethereum gas fees")
        fees_embed.add_field(name="Fastest", value="`{} gwei`".format(fees["fastest"] / 10))
        fees_embed.add_field(name="Fast (< 2m)", value="`{} gwei`".format(fees["fast"] / 10))
        fees_embed.add_field(name="Standard (< 5m)", value="`{} gwei`".format(fees["average"] / 10))
        await ctx.send(embed=fees_embed)
        pass


def bull_or_bear(percentage):
    if "-" in percentage:  # why would you do this
        return discord.Color.red()
    else:
        return discord.Color.green()


def setup(client):
    client.add_cog(CryptoCurrency(client))
