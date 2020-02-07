from mongoengine import *


class RemindListDocument(Document):
    user_id = IntField(required=True)
    reminds = ListField()


class RemindDocument(EmbeddedDocument):
    remind_text = StringField(required=True)
    remind_date = DateTimeField(required=True)


def init(user_id):
    doc = RemindListDocument(user_id=user_id).save()
    return doc


def get(user_id):
    try:
        target_document = RemindListDocument.objects().get(user_id=user_id)
        return target_document
    except DoesNotExist:
        new_document = init(user_id)
        return new_document


def add(user_id, remind):
    target_document = get(user_id)
    target_document.reminds.append(remind)
    target_document.save()


def remove(user_id, index):
    target_document = get(user_id)
    target_document.reminds.pop(index)
    target_document.save()
