import mongo_setup

players = mongo_setup.db["players"]

def AddPlayer(discordID: str, steamID: str):
    print(discordID, steamID)
    curPlayer = GetPlayer(discordID)
    print(curPlayer)
    if curPlayer is None:
        InsertOnePlayer(discordID, steamID)
    else:
        steamIdList = list(curPlayer["steamID"])
        if steamID not in steamIdList:
            steamIdList.append(steamID)
            UpdateOnePlayer(discordID, steamIdList)
        else:
            return False
    return True


def GetPlayer(discordID: str):
    curPlayer = players.find_one({"discordID" : discordID})
    return curPlayer

def GetPlayerSteamId(discordID: str):
    curPlayer = GetPlayer(discordID)
    if curPlayer is None:
        return None
    else:
        return list(curPlayer["steamID"])[0]

def InsertOnePlayer(discordID: str, steamID: str):
    players.insert_one({"discordID": discordID, "steamID": [steamID]})

def UpdateOnePlayer(discordID: str, steamIdList):
    players.update_one({"discordID" : discordID}, { "$set": { "steamID": steamIdList } })
    