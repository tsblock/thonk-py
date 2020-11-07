from mongoengine import *


class GuildSettings(Document):
    guild_id = IntField(required=True)
    dumb_message = BooleanField(default=False)


def init(guild_id):
    doc = GuildSettings(guild_id=guild_id).save()
    return doc


def get(guild_id):
    try:
        target_document = GuildSettings.objects().get(guild_id=guild_id)
        return target_document
    except DoesNotExist:
        new_document = init(guild_id)
        return new_document
