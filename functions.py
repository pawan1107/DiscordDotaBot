import constant.constant as const
import re

def GetNickName(name):
  if name in const.pros:
    return "Pro"
  return "Noob"

def isInstanceDiscordId(playerID):
  trimID = playerID[:3]+playerID[-1]
  return trimID == "<@!>"

def getOnlyId(playerID):
  print(re.sub(r"\D", "", playerID))
  return re.sub(r"\D", "", playerID)