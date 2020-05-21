import discord
import httpx
from discord.ext import commands

import config

base_url = "https://api.openweathermap.org/data/2.5/"
api_key = config.openweather_key


class Weather(commands.Cog, name="Weather"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="weather", description="Get current weather infomation", usage="<city name>")
    async def weather(self, ctx, *, city_name):
        data = await get_current_weather_data(city_name)
        main_data = data["main"]
        celsius = main_data["temp"]
        fahrenheit = c_to_f(celsius)
        humidity = main_data["humidity"]
        min_celsius = main_data["temp_min"]
        max_celsius = main_data["temp_max"]
        min_fahrenheit = c_to_f(min_celsius)
        max_fahrenheit = c_to_f(max_celsius)
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        weather_embed = discord.Embed(
            title=data["name"],
            description=data["weather"][0]["main"],
            color=discord.Color.blue()
        )
        weather_embed.set_thumbnail(
            url="https://openweathermap.org/img/wn/{}@2x.png".format(data["weather"][0]["icon"]))
        weather_embed.add_field(name="🌡 Temperature", value="{}°C / {}°F".format(celsius, fahrenheit))
        weather_embed.add_field(name="🌡 Temperature range", value="{}°C - {}°C\n"
                                                                   "{}°F - {}°F".format(min_celsius, max_celsius,
                                                                                        min_fahrenheit, max_fahrenheit))
        weather_embed.add_field(name="💨 Wind Speed", value="{} m/s".format(wind_speed))
        weather_embed.add_field(name="💨 Wind Direction", value="{}°".format(wind_deg))
        weather_embed.add_field(name="💧 Humidity", value="{}%".format(humidity))
        await ctx.send(embed=weather_embed)

    # @commands.command(name="forecast", description="Get 5-day weather forecast", usage="<city name>")
    # async def forecast(self, ctx, *, city_name):
    #     pass


async def get_current_weather_data(city_name):
    async with httpx.AsyncClient() as client:
        req = await client.get(base_url + "weather", params={
            "q": city_name,
            "units": "metric",
            "appid": api_key
        })
        if not req.is_error:
            return req.json()
        else:
            return None


def c_to_f(c):
    return round((c * 1.8) + 32)


def setup(client):
    client.add_cog(Weather(client))
