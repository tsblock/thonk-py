import asyncio
import io
import time
from difflib import SequenceMatcher
from typing import Optional

import discord
import httpx
import qrcode
from discord.ext import commands

import config
from utils import funcs


class Utility(commands.Cog, name="Utility"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="urban", description="Urban Dictionary, but in Discord.", usage="<term>")
    @commands.cooldown(5, 5, commands.BucketType.default)
    async def urban(self, ctx, *, term):
        params = {"term": term}
        await ctx.trigger_typing()
        async with httpx.AsyncClient() as client:
            res = await client.get("http://api.urbandictionary.com/v0/define", params=params)
        data = res.json()["list"]
        if len(data) == 0:
            await ctx.channel.send(embed=funcs.error_embed(None, "Term does not exist."))
        else:
            urban_embed = discord.Embed(
                color=discord.Color.from_rgb(255, 255, 0),
                title=term
            )
            definition = data[0]["definition"].replace("[", "").replace("]", "")[:2000] + "..."
            example = data[0]["example"].replace("[", "").replace("]", "")
            thumbs_up = data[0]["thumbs_up"]
            thumbs_down = data[0]["thumbs_down"]
            author = data[0]["author"]
            urban_embed.add_field(name="Definition", value=definition)
            if example:
                urban_embed.add_field(name="Example", value=example)
            urban_embed.set_footer(text="👍 {} | 👎 {} | By: {}".format(str(thumbs_up), str(thumbs_down), author))
            await ctx.channel.send(embed=urban_embed)
            # TODO: add reaction menu

    @commands.command(name="wpm", description="Test your typing speed.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wpm(self, ctx):
        await ctx.trigger_typing()
        async with httpx.AsyncClient() as client:
            res = await client.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
            full_extract = res.json()["extract"].split()[:49]
            extract = " ".join(full_extract)
        await ctx.send(content=extract.replace(" ", " ឵឵឵"))
        start_time = time.time()
        try:
            msg = await self.client.wait_for("message", timeout=120.0, check=lambda
                x: x.channel.id == ctx.channel.id and x.author.id == ctx.author.id)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Times out! Type faster next time.")
        else:
            input_text = msg.content
            if "឵឵឵" not in input_text:
                if similar(extract, input_text) < 0.5:
                    await ctx.send(embed=funcs.error_embed(None, "You have made too many errors!"))
                    return
                end_time = time.time()
                delta_time = end_time - start_time
                count = 0
                for i, c in enumerate(extract):
                    if input_text[i] == c:
                        count += 1
                    else:
                        continue
                accuracy = round(count / len(extract) * 100, 2)
                wpm = round(len(input_text) * 60 / (5 * delta_time), 2)

                await ctx.send("**WPM:** {}\n"
                               "**Accuracy: ** {}%".format(wpm, accuracy))

    # by ryancflam (https://github.com/ryancflam)
    @commands.command(name="covid19", description="Check the current state of the coronavirus pandemic",
                      usage="[city name]", aliases=["corona", "coronavirus", "cv"])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def covid(self, ctx, *, city: Optional[str] = None):
        headers = {"x-rapidapi-host": "corona-virus-world-and-india-data.p.rapidapi.com",
                   "x-rapidapi-key": config.rapidapi_key}
        await ctx.trigger_typing()
        async with httpx.AsyncClient()as session:
            r = await session.get("https://corona-virus-world-and-india-data.p.rapidapi.com/api", headers=headers)
            data = r.json()
        total = data["countries_stat"]
        found = False
        if city is None:
            total = data["world_total"]
        else:
            if city.casefold().startswith("united states") or city.casefold().startswith("america"):
                city = "usa"
            elif city.casefold().startswith("united kingdom") or city.casefold().startswith(
                    "great britain") or city.casefold().startswith("britain") or city.casefold().startswith("england"):
                city = "uk"
            elif city.casefold().startswith("hk"):
                city = "hong kong"
            if city.casefold().startswith("korea") or city.casefold().startswith(
                    "south korea") or city.casefold().startswith("sk"):
                city = "S. Korea"
            for x in total:
                if x["country_name"].casefold().replace(".", "") == city.casefold().replace(".", ""):
                    found = True
                    break
            if not found:
                total = data["world_total"]
            else:
                total = x  # what
        corona_embed = discord.Embed(color=discord.Color(0x23272A),
                                     title=f"COVID-19 Stats ({total['country_name'] if found else 'Global'})",
                                     description="Statistics taken at: " + data["statistic_taken_at"] + " UTC")
        corona_embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/SARS-CoV-2_without_background.png/220px-SARS-CoV-2_without_background.png")
        if found:
            corona_embed.add_field(name="Country", value=total["country_name"])
            corona_embed.add_field(name="Total Cases", value=total["cases"])
            corona_embed.add_field(name="Total Deaths", value=total[
                                                                  "deaths"] + f"\n({round(int(total['deaths'].replace(',', '').replace('N/A', '0')) / int(total['cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
            corona_embed.add_field(name="Total Recovered", value=total[
                                                                     "total_recovered"] + f"\n({round(int(total['total_recovered'].replace(',', '').replace('N/A', '0')) / int(total['cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
            corona_embed.add_field(name="Active Cases", value=total[
                                                                  "active_cases"] + f"\n({round(int(total['active_cases'].replace(',', '').replace('N/A', '0')) / int(total['cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
            corona_embed.add_field(name="Critical Cases", value=total["serious_critical"])
            corona_embed.add_field(name="Total Tests", value=total["total_tests"])
        else:
            corona_embed.add_field(name="Total Cases", value=total["total_cases"])
            corona_embed.add_field(name="Total Deaths", value=total[
                                                                  "total_deaths"] + f"\n({round(int(total['total_deaths'].replace(',', '').replace('N/A', '0')) / int(total['total_cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
            corona_embed.add_field(name="Total Recovered", value=total[
                                                                     "total_recovered"] + f"\n({round(int(total['total_recovered'].replace(',', '').replace('N/A', '0')) / int(total['total_cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
            corona_embed.add_field(name="Active Cases", value=total[
                                                                  "active_cases"] + f"\n({round(int(total['active_cases'].replace(',', '').replace('N/A', '0')) / int(total['total_cases'].replace(',', '').replace('N/A', '0')) * 100, 2)}%)")
        corona_embed.add_field(name="New Cases Today", value=total["new_cases"])
        corona_embed.add_field(name="New Deaths Today", value=total["new_deaths"])
        corona_embed.set_footer(text="Note: The data provided may not be 100% accurate.")
        await ctx.send(embed=corona_embed)

    @commands.command(name="qrcode", description="Generate an qr code", usage="<text/url>", aliases=["qr", "qrc"])
    async def qrcode(self, ctx, *, data):
        qr = qrcode.QRCode(
            box_size=20
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")

        img_bytes.seek(0)
        print(img_bytes)
        await ctx.send(file=discord.File(img_bytes, filename="qr.png"))

    @commands.cooldown(1, 20, commands.BucketType.channel)
    @commands.command(name="wolfram_alpha", description="Get result from Wolfram Alpha.", usage="<query>",
                      aliases=["wolf"])
    async def wolf(self, ctx, *, query):
        await ctx.trigger_typing()
        request_params = {
            "output": "json",
            "appid": config.wolfram_alpha_app_id,
            "lang": "en",
            "input": query
        }
        result = await funcs.simple_get_request("https://api.wolframalpha.com/v2/query", params=request_params)
        # get pods (result)
        pods = []
        for pod in result["queryresult"]["pods"]:
            img = []
            img.append(pod["title"])
            for subpod in pod["subpods"]:
                img.append(subpod["img"]["src"])
            pods.append(img)
        embeds = []
        for pod in pods:
            title = pod[0]
            imgs = pod[1:]
            embed = discord.Embed(title=title, color=discord.Color.blurple())
            embed.set_image(url=imgs[0])  # get the first image link for now
            embeds.append(embed)
            # what in the fuck
            if len(imgs) > 1:
                extra_imgs = imgs[1:]
                for extra_img in extra_imgs:
                    extra_embed = discord.Embed(title=title, color=discord.Color.blurple())
                    extra_embed.set_image(url=extra_img)
                    embeds.append(extra_embed)
        for embed in embeds:
            await ctx.send(embed=embed)
            await asyncio.sleep(0.5)
        pass



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def setup(client):
    client.add_cog(Utility(client))
