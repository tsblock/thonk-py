import typing
from datetime import datetime

import discord
import parsedatetime
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

import config
from database import reminder
from utils import funcs

job_stores = {
    "default": MongoDBJobStore(host=config.mongodb_url, collection="reminder_jobs", database="thonk")
}

scheduler = AsyncIOScheduler(
    jobstores=job_stores
)


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler.start()

    async def send_remind(self, user_id, remind_text, job_id):
        user = self.client.get_user(user_id)
        if not user:
            return
        remind_embed = discord.Embed(
            color=discord.Color.from_rgb(255, 255, 0),
            title="Reminder",
            description="Hello {}!\n"
                        "I'm here to remind you:\n"
                        "```{}```".format(user.name, remind_text)
        )
        scheduler.remove_job(job_id)
        await user.send(embed=remind_embed)

    @commands.command(name="remindlist", description="List your reminders", aliases=["rlist"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remind_list(self, ctx):
        pass

    @commands.command(name="remindme", description="Remind you things I guess.",
                      usage="\"<date>\" [repeat? true/false] <text>\n"
                            "For the date argument, take a look at https://www.reddit.com/r/RemindMeBot/comments/2862bd/remindmebot_date_options/\n"
                            "You MUST put quote in between the date argument!",
                      aliases=["remind"])
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def remindme(self, ctx, date_text, repeat: typing.Optional[bool] = False, *, remind_text):
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(date_text)
        if parse_status == 0:
            await ctx.send(embed=funcs.errorEmbed(None, "Please enter a valid date option!"))
            return

        # convert datetime to utc
        # stupid timezone
        date = datetime(*time_struct[:6])
        epoch = datetime(1970, 1, 1)
        date = datetime.fromtimestamp((date - epoch).total_seconds())

        new_remind = reminder.RemindDocument(remind_text=remind_text, remind_date=date, repeat=repeat)
        reminder.add(ctx.author.id, new_remind)

        remind_embed = discord.Embed(
            color=discord.Color.from_rgb(255, 255, 0),
            description="👌 I will remind you at `{} UTC`".format(str(date))
        )
        await ctx.send(embed=remind_embed)

    @commands.command(name="remind_delete", description="Delete a reminder", usage="<id>",
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


def setup(client):
    client.add_cog(Reminder(client))
