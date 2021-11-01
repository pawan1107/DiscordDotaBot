import mongoengine
from model.guilds import Guild

class User(mongoengine.Document):
  _id = mongoengine.IntField(required=True)
  name = mongoengine.StringField(required=True)
  bot =  mongoengine.BooleanField(default=False)
  playerIdList = mongoengine.ListField()
  displayName = mongoengine.StringField(required=True)
  guild = mongoengine.EmbeddedDocumentListField(Guild)

  meta = {
      'db_alias': 'core',
      'collection': 'users'
  }