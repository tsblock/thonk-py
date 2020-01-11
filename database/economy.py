from mongoengine import *


class EconomyDocument(Document):
    user_id = IntField(required=True)
    balance = IntField(default=0)
    last_daily: DateTimeField()


def init(user_id):
    target_document = EconomyDocument(user_id=user_id)
    target_document.save()
    return target_document


def get(user_id):
    target_document = EconomyDocument.objects().get(user_id=user_id)
    if not target_document:
        target_document = init(user_id)
    return target_document


def add(user_id, value):
    target_document = EconomyDocument.objects().get(user_id=user_id)
    if not target_document:
        target_document = init(user_id)
    target_document.balance += value
    target_document.save()
