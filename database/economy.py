from mongoengine import *


class EconomyDocument(Document):
    user_id = IntField(required=True)
    balance = IntField(default=0)
    last_daily: DateTimeField(default=None)


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
    target_document = EconomyDocument.objects().get(user_id=user_id)
    if not target_document:
        target_document = init(user_id)
    target_document.balance += value
    target_document.save()
