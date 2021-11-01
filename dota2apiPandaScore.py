import requests
import json
import os
from collections import namedtuple 
import dill



URL = "https://api.pandascore.co/dota2/"
PANDA_SCORE_TOKEN = os.getenv("TOKEN_PANDA_SCORE")
FILE_NAME = "dota2Heros.pickle"
heroesList = []

def customDecoder(geekDict): 
    return namedtuple('X', geekDict.keys())(*geekDict.values()) 

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def GetRequest(endPoint, parameter = ""):
  response = requests.get(URL+endPoint, headers={"Authorization": PANDA_SCORE_TOKEN}, params=parameter)
  return response.json()
  # print(jprint(response.json()))

def GetAllHeroesListFromApi():
  parameter1 = {"sort": "id", "per_page":200, "page":1}
  parameter2 = {"sort": "id", "per_page":200, "page":2}
  page1 = list(GetRequest("heroes", parameter1))
  page2 = list(GetRequest("heroes", parameter2))
  heroesList = page1+page2
  return heroesList

def saveHeroListToFile(heroesList):
  dill.dump(heroesList, file = open(FILE_NAME, "wb"))


def getSavedHeroList():
  heroesList = dill.load(open(FILE_NAME, "rb"))
  return heroesList

def GetAllHeros():
  if not heroesList:
    heroes = GetAllHeroesListFromApi()
    saveHeroListToFile(heroes)
    return heroes
  else:
    return heroesList


GetAllHeros()