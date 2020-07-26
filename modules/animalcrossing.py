# code mostly by ryancflam (https://github.com/ryancflam)

import json

import discord
from discord.ext import commands

from utils import funcs


class AnimalCrossing(commands.Cog, name="Animal Crossing"):
    def __init__(self, client):
        self.client = client
        self.bugs = json.load(open("assets/acnhbugs.json", "r", encoding="utf8"))
        self.fish = json.load(open("assets/acnhfish.json", "r", encoding="utf8"))
        self.sea = json.load(open("assets/acnhsea.json", "r", encoding="utf8"))
        self.villagers = json.load(open("assets/acnhvillagers.json", "r", encoding="utf8"))

    @commands.command(name="acnhbugs", description="Shows information about an Animal Crossing: New Horizons bug!",
                      usage="<bug name>", aliases=["acb", "acnhb"])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def acbugs(self, ctx, *, bug):
        try:
            bugdata = self.bugs[bug.casefold().replace(" ", "_").replace("'", "").replace("‘", "").replace("’", "")]
        except KeyError:
            await ctx.send(embed=funcs.error_embed(None, "Bug not found!"))
        else:
            bugname = str(bugdata["name"]["name-USen"]).title().replace("'S", "'s")
            northmonths = bugdata["availability"]["month-northern"] if bugdata["availability"][
                                                                           "month-northern"] != "" else "All Year"
            southmonths = bugdata["availability"]["month-southern"] if bugdata["availability"][
                                                                           "month-southern"] != "" else "All Year"
            time = bugdata["availability"]["time"] if bugdata["availability"]["time"] != "" else "All Day"
            price = bugdata["price"]
            flickprice = bugdata["price-flick"]
            catch = '"{}"'.format(bugdata["catch-phrase"])
            location = bugdata["availability"]["location"]
            rarity = bugdata["availability"]["rarity"]
            image = "http://acnhapi.com/v1/images/bugs/{}".format(bugdata["id"])
            bug_embed = discord.Embed(title=f"{bugname}", description=catch, color=discord.Color(0x23272A))
            bug_embed.set_image(url=image)
            bug_embed.set_thumbnail(
                url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d8fe0719-55c2-4775-9ea5-fa68ad28d089/dd98bnh-cdaa0e7e-c5f1-45f9-99fb-5a22d3c2974b.png/v1/fill/w_902,h_599,strp/transparent_animal_crossing__new_horizons_logo_by_sethwilliamson_dd98bnh-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD01OTkiLCJwYXRoIjoiXC9mXC9kOGZlMDcxOS01NWMyLTQ3NzUtOWVhNS1mYTY4YWQyOGQwODlcL2RkOThibmgtY2RhYTBlN2UtYzVmMS00NWY5LTk5ZmItNWEyMmQzYzI5NzRiLnBuZyIsIndpZHRoIjoiPD05MDIifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.31cbh56MpeGiy5KJU98jru7tlA-31GmdLJxRJ17Cbp8")
            bug_embed.add_field(name="Location", value=location)
            bug_embed.add_field(name="Rarity", value=rarity)
            bug_embed.add_field(name="Northern Months", value=northmonths)
            bug_embed.add_field(name="Southern Months", value=southmonths)
            bug_embed.add_field(name="Time", value=time)
            bug_embed.add_field(name="Selling Price", value=price)
            bug_embed.add_field(name="Selling Price (Flick)", value=flickprice)
            await ctx.send(embed=bug_embed)

    @commands.command(name="acfish", description="Shows information about an Animal Crossing: New Horizons fish!",
                      usage="<fish name>", aliases=["acf", "acnhf"])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def acfish(self, ctx, *, fish):
        try:
            fishdata = self.fish[fish.casefold().replace(" ", "_").replace("'", "").replace("‘", "").replace("’", "")]
        except KeyError:
            await ctx.send(embed=funcs.error_embed(None, "Fish not found!"))
        else:
            fishname = str(fishdata["name"]["name-USen"]).title().replace("'S", "'s")
            shadow = fishdata["shadow"]
            northmonths = fishdata["availability"]["month-northern"] if fishdata["availability"][
                                                                            "month-northern"] != "" else "All Year"
            southmonths = fishdata["availability"]["month-southern"] if fishdata["availability"][
                                                                            "month-southern"] != "" else "All Year"
            time = fishdata["availability"]["time"] if fishdata["availability"]["time"] != "" else "All Day"
            price = fishdata["price"]
            cjprice = fishdata["price-cj"]
            catch = '"{}"'.format(fishdata["catch-phrase"])
            location = fishdata["availability"]["location"]
            rarity = "EVERYWHERE GODDAMMIT" if "Bass" in fishname else fishdata["availability"]["rarity"]
            image = "http://acnhapi.com/v1/images/fish/{}".format(fishdata["id"])
            fish_embed = discord.Embed(title=f"{fishname}", description=catch, color=discord.Color(0x23272A))
            fish_embed.set_image(url=image)
            fish_embed.set_thumbnail(
                url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d8fe0719-55c2-4775-9ea5-fa68ad28d089/dd98bnh-cdaa0e7e-c5f1-45f9-99fb-5a22d3c2974b.png/v1/fill/w_902,h_599,strp/transparent_animal_crossing__new_horizons_logo_by_sethwilliamson_dd98bnh-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD01OTkiLCJwYXRoIjoiXC9mXC9kOGZlMDcxOS01NWMyLTQ3NzUtOWVhNS1mYTY4YWQyOGQwODlcL2RkOThibmgtY2RhYTBlN2UtYzVmMS00NWY5LTk5ZmItNWEyMmQzYzI5NzRiLnBuZyIsIndpZHRoIjoiPD05MDIifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.31cbh56MpeGiy5KJU98jru7tlA-31GmdLJxRJ17Cbp8")
            fish_embed.add_field(name="Shadow", value=shadow)
            fish_embed.add_field(name="Location", value=location)
            fish_embed.add_field(name="Rarity", value=rarity)
            fish_embed.add_field(name="Northern Months", value=northmonths)
            fish_embed.add_field(name="Southern Months", value=southmonths)
            fish_embed.add_field(name="Time", value=time)
            fish_embed.add_field(name="Selling Price", value=price)
            fish_embed.add_field(name="Selling Price (C.J.)", value=cjprice)
            await ctx.send(embed=fish_embed)

    @commands.command(name="acsea",
                      description="Shows information about an Animal Crossing: New Horizons sea creature!",
                      usage="<sea creature name>", aliases=["acs", "acnhs"])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def acsea(self, ctx, *, sea):
        try:
            seadata = self.sea[sea.casefold().replace(" ", "_").replace("'", "").replace("‘", "").replace("’", "")]
        except KeyError:
            await ctx.send(embed=funcs.error_embed(None, "Sea creature not found!"))
        else:
            fishname = str(seadata["name"]["name-USen"]).title().replace("'S", "'s")
            shadow = seadata["shadow"]
            speed = seadata["speed"]
            northmonths = seadata["availability"]["month-northern"] if seadata["availability"][
                                                                           "month-northern"] != "" else "All Year"
            southmonths = seadata["availability"]["month-southern"] if seadata["availability"][
                                                                           "month-southern"] != "" else "All Year"
            time = seadata["availability"]["time"] if seadata["availability"]["time"] != "" else "All Day"
            price = seadata["price"]
            image = "http://acnhapi.com/v1/images/sea/{}".format(seadata["id"])
            sea_embed = discord.Embed(title=f"{fishname}", color=discord.Color(0x23272A))
            sea_embed.set_image(url=image)
            sea_embed.set_thumbnail(
                url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d8fe0719-55c2-4775-9ea5-fa68ad28d089/dd98bnh-cdaa0e7e-c5f1-45f9-99fb-5a22d3c2974b.png/v1/fill/w_902,h_599,strp/transparent_animal_crossing__new_horizons_logo_by_sethwilliamson_dd98bnh-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD01OTkiLCJwYXRoIjoiXC9mXC9kOGZlMDcxOS01NWMyLTQ3NzUtOWVhNS1mYTY4YWQyOGQwODlcL2RkOThibmgtY2RhYTBlN2UtYzVmMS00NWY5LTk5ZmItNWEyMmQzYzI5NzRiLnBuZyIsIndpZHRoIjoiPD05MDIifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.31cbh56MpeGiy5KJU98jru7tlA-31GmdLJxRJ17Cbp8")
            sea_embed.add_field(name="Shadow", value=shadow)
            sea_embed.add_field(name="Speed", value=speed)
            sea_embed.add_field(name="Northern Months", value=northmonths)
            sea_embed.add_field(name="Southern Months", value=southmonths)
            sea_embed.add_field(name="Time", value=time)
            sea_embed.add_field(name="Selling Price", value=price)
            await ctx.send(embed=sea_embed)

    @commands.command(name="acvillager",
                      description="Shows information about an Animal Crossing: New Horizons villagers!",
                      usage="<villager name>", aliases=["acv", "acnhv"])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def acvillager(self, ctx, villager):
        # what the fuck is this ryan
        found = False
        for vid in list(self.villagers):
            villagerdata = self.villagers[vid]
            if str(villagerdata["name"]["name-USen"]).casefold().replace(" ", "_") == villager.casefold().replace(" ",
                                                                                                                  "_"):
                found = True
                break
        if not found:
            await ctx.send(embed=funcs.error_embed(None, "Villager not found!"))
            return

        bugname = str(villagerdata["name"]["name-USen"]).title()
        personality = villagerdata["personality"]
        birth = villagerdata["birthday-string"]
        species = villagerdata["species"]
        gender = villagerdata["gender"]
        phrase = villagerdata["catch-phrase"]
        image = "http://acnhapi.com/v1/images/villagers/{}".format(villagerdata["id"])
        villager_embed = discord.Embed(title=f"{bugname}", color=discord.Color(0x23272A))
        villager_embed.set_image(url=image)
        villager_embed.set_thumbnail(
            url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d8fe0719-55c2-4775-9ea5-fa68ad28d089/dd98bnh-cdaa0e7e-c5f1-45f9-99fb-5a22d3c2974b.png/v1/fill/w_902,h_599,strp/transparent_animal_crossing__new_horizons_logo_by_sethwilliamson_dd98bnh-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD01OTkiLCJwYXRoIjoiXC9mXC9kOGZlMDcxOS01NWMyLTQ3NzUtOWVhNS1mYTY4YWQyOGQwODlcL2RkOThibmgtY2RhYTBlN2UtYzVmMS00NWY5LTk5ZmItNWEyMmQzYzI5NzRiLnBuZyIsIndpZHRoIjoiPD05MDIifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.31cbh56MpeGiy5KJU98jru7tlA-31GmdLJxRJ17Cbp8")
        villager_embed.add_field(name="Personality", value=personality)
        villager_embed.add_field(name="Birthday", value=birth)
        villager_embed.add_field(name="Species", value=species)
        villager_embed.add_field(name="Gender", value=gender)
        villager_embed.add_field(name="Initial Phrase", value='"{}"'.format(phrase))
        await ctx.send(embed=villager_embed)


def setup(client):
    client.add_cog(AnimalCrossing(client))
