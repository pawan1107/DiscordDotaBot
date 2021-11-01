import requests
import json
import os
from collections import namedtuple 
import dill
import CustomExceptions as ce


URL = "https://api.opendota.com/api/"
FILE_NAME = "dota2Heros.pickle"
heroes = {}
# os.system("cls" if os.name == "nt" else "clear")

def customDecoder(geekDict): 
    return namedtuple('X', geekDict.keys())(*geekDict.values()) 


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def GetRequest(endPoint, parameter = ""):
  response = requests.get(URL+endPoint, params=parameter)
  return response.json()
  # print(jprint(response.json()))

def GetRequestObject(endPoint, parameter = ""):
  response = requests.get(URL+endPoint, params=parameter)
  print(endPoint)
  return response.json(object_hook=customDecoder)

def GetAllHeroesListFromApi():
  heroesList = list(GetRequest("heroes"))
  return heroesList

def saveHeroListToFile(heroesList):
  dill.dump(heroesList, file = open(FILE_NAME, "wb"))


def getSavedHeroList():
  heroesDict = dill.load(open(FILE_NAME, "rb"))
  return heroesDict

def GetHeroConstant():
    heroesList = GetRequest("constants/heroes")
    heroesDict = {value["id"]: json.loads(json.dumps(value), object_hook=customDecoder) for key, value in heroesList.items()}
    # saveHeroListToFile(heroesDict)
    return heroesDict
  
def GetItemConstant():
    itemList = GetRequest("constants/items")
    itemDict = {value["id"]: json.loads(json.dumps(value), object_hook=customDecoder) for key, value in itemList.items()}
    # saveHeroListToFile(itemDict)
    return itemDict

def GetPlayerStats(playerId: int):
  player = GetRequestObject(f"players/{playerId}")
  if hasattr(player, 'error') or not hasattr(player, 'profile'):
    raise ce.PlayerIdNotFound(playerId)
  return player

def GetPlayerOverallWinLose(playerId: int):
  player = GetRequestObject(f"players/{playerId}/wl")
  if hasattr(player, 'error') or (player.lose == 0 and player.win == 0) :
    raise ce.PlayerIdNotFound(playerId)
  return player

def GetPlayerRecentMatch(playerId: int):
  player = GetRequestObject(f"players/{playerId}/recentMatches")
  if hasattr(player, 'error') or len(player) == 0:
    raise ce.PlayerIdNotFound(playerId)
  return player

def GetPlayerAllMatch(playerId: int):
  player = GetRequestObject(f"players/{playerId}/matches")
  if hasattr(player, 'error') or len(player) == 0:
    raise ce.PlayerIdNotFound(playerId)
  return player

def GetPlayerAllHeroStats(playerId: int):
  player = GetRequestObject(f"players/{playerId}/matches")
  return player

def GetMatchDetails(matchId: int):
  match = GetRequestObject(f"matches/{matchId}")
  if "error" in match:
    raise ce.MatchIdNotFound(matchId)
  return match
