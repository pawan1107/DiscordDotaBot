import mongoengine

class Guild(mongoengine.EmbeddedDocument):
  _id = mongoengine.IntField(required=True)
  name = mongoengine.StringField(required=True)