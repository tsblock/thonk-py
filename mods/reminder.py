from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

import config

jobstores = {
    "default": MongoDBJobStore(host=config.mongodb_url, collection="reminder")
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores
)


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler.start()


def setup(client):
    client.add_cog(Reminder(client))
