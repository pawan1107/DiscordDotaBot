import json
from collections import namedtuple 
import dota2apiOpenDota as d2a

def customDecoder(geekDict): 
    return namedtuple('X', geekDict.keys())(*geekDict.values()) 

with open('dotaconstants/game_mode.json') as myfile:
    GAME_MODE = json.load(myfile)

with open('dotaconstants/lobby_type.json') as myfile:
    LOBBY_TYPE = json.load(myfile)

HEROES = d2a.GetHeroConstant()
ITEMS = d2a.GetItemConstant()
