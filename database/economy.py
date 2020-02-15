from datetime import datetime

from mongoengine import *


class EconomyDocument(Document):
    user_id = IntField(required=True)
    balance = IntField(default=0)
    next_daily = DateTimeField(default=datetime.utcnow())
    daily_streak = IntField(default=0)


def init(user_id):
    doc = EconomyDocument(user_id=user_id).save()
    return doc


def get(user_id):
    try:
        target_document = EconomyDocument.objects().get(user_id=user_id)
        return target_document
    except DoesNotExist:
        new_document = init(user_id)
        return new_document


def add(user_id, value):
    target_document = get(user_id)
    target_document.balance += value
    target_document.save()
