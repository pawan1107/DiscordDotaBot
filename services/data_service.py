from model.users import User
from model.guilds import Guild
from typing import List

def AddUser(
  id: int,
  name: str,
  bot: bool,
  playerId: int,
  displayName: str,
  guildId: int,
  guildName: str
) -> User:
  user = User()
  user._id = id
  user.name = name
  user.bot = bot
  user.displayName = displayName
  user.playerIdList.append(playerId)

  guild = Guild()
  guild.name = guildName
  guild._id = guildId

  user.guild.append(guild)

  user.save();
  return user

def GetUserById(id: int) -> User:
  user = User.objects(_id=id).first()
  return user


def GetPlayerIdOfUser(id: int) -> List[int]:
  user = GetUserById(id)
  return user.playerIdList

def AddUserPlayerId(id:int, playerId: int):
  user = GetUserById(id)
  user.playerIdList.append(playerId)
  user.save();

def AddUserGuild(id:int, guildId: int, guildName: str):
  user = GetUserById(id)
  guild = Guild()
  guild.name = guildName
  guild._id = guildId

  user.guild.append(guild)
  user.save();