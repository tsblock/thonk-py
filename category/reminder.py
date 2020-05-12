from datetime import datetime

import discord
import parsedatetime
from discord.ext import commands, tasks

from database import reminder
from utils import funcs


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reminder_loop.start()

    @commands.command(name="remindlist", description="List your reminders", aliases=["rlist"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remind_list(self, ctx):
        target_document = reminder.get(ctx.author.id)
        list_embed = discord.Embed(
            color=discord.Color.from_rgb(255, 255, 0),
            title="📃 List of reminders",
        )
        if len(target_document.reminds) == 0:
            list_embed.description = "None. Create one with {}remindme.".format(self.client.command_prefix)
        else:
            index = 0
            for remind in target_document.reminds:
                list_embed.add_field(name="**{}. ** `{}`".format(index, remind.remind_text),
                                     value="Trigger time: `{}`".format(str(remind.remind_date)))
                index += 1
        await ctx.send(embed=list_embed)

    @commands.command(name="remindme", description="Remind you things I guess.",
                      usage="\"<date>\" <text>\n"
                            "For the date argument, take a look at https://www.reddit.com/r/RemindMeBot/comments/2862bd/remindmebot_date_options/\n"
                            "You MUST put quote in between the date argument!",
                      aliases=["remind"])
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def remindme(self, ctx, date_text: str, *, remind_text: str):
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(date_text, datetime.utcnow())
        date = datetime(*time_struct[:6])
        if parse_status == 0:
            await ctx.send(embed=funcs.errorEmbed(None, "Please enter a valid date option!"))
            return
        new_remind = reminder.RemindDocument(remind_text=remind_text, remind_date=date)
        reminder.add(ctx.author.id, new_remind)
        remind_embed = discord.Embed(
            color=discord.Color.from_rgb(255, 255, 0),
            description="👌 I will remind you at `{} UTC`\n\n"
                        "⚠ **Reminder might be unreliable, use it at your own risk!**\n"
                        "**This might be fixed soon\™**".format(str(date))
        )
        await ctx.send(embed=remind_embed)

    @commands.command(name="reminddelete", description="Delete a reminder", usage="<id>",
                      aliases=["delremind", "reminddel"])
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def remind_delete(self, ctx, reminder_id: int):
        target_document = reminder.get(ctx.author.id)
        if reminder_id > len(target_document.reminds):
            await ctx.send(embed=funcs.errorEmbed(None, "Reminder does not exist!"))
            return
        reminder.remove(ctx.author.id, reminder_id)
        success_embed = discord.Embed(
            color=discord.Color.green(),
            description="{} **Reminder deleted**".format(funcs.emotes["tick"])
        )
        await ctx.send(embed=success_embed)

    # FIXME this loop sometimes stops working for no reason
    @tasks.loop(seconds=10.0)
    async def reminder_loop(self):
        documents = reminder.RemindListDocument.objects()
        for document in documents:
            for remind in document.reminds:
                if datetime.utcnow() >= remind.remind_date:
                    user_id = document.user_id
                    user = self.client.get_user(user_id)
                    if not user:
                        return
                    remind_embed = discord.Embed(
                        color=discord.Color.from_rgb(255, 255, 0),
                        title="Reminder",
                        description="Hello {}!\n"
                                    "I'm here to remind you:\n"
                                    "```{}```".format(user.name, remind.remind_text)
                    )
                    await user.send(embed=remind_embed)
                    reminder.remove(user_id, document.reminds.index(remind))

    @reminder_loop.before_loop
    async def before_loop(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Reminder(client))
