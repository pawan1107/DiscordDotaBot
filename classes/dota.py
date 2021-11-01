import loadConstant as const
class Match:

    def __init__(self, matchData):
        self.radiant_win = matchData["radiant_win"]
        self.match_id = matchData["match_id"]
        self.duration = matchData["duration"]
        self.radiant_score = matchData["radiant_score"]
        self.dire_score = matchData["dire_score"]
        self.players = [Dotaplayer(player) for player in sorted(matchData["players"], key=lambda x: x["player_slot"])]


  
class Dotaplayer:

    def __init__(self, playerData):
        self.personaname = playerData["personaname"] if "personaname" in playerData else "anonymous"
        self.player_slot = playerData["player_slot"]
        self.kills = playerData["kills"]
        self.deaths = playerData["deaths"]
        self.assists = playerData["assists"]
        self.items=  [playerData["item_0"], playerData["item_1"], playerData["item_2"], playerData["item_3"], playerData["item_4"], playerData["item_5"]]
        self.hero_id = playerData["hero_id"]
        self.net_worth = playerData["net_worth"]
        self.xp_per_min = playerData["xp_per_min"]
        self.gold_per_min = playerData["gold_per_min"]
        self.last_hits = playerData["last_hits"]
        self.denies = playerData["denies"]
        self.hero_damage = playerData["hero_damage"]
        self.tower_damage = playerData["tower_damage"]
        self.hero_healing = playerData["hero_healing"]

    def GetPlayerItemNames(self):
        itemName = [const.ITEMS[itemId].dname for itemId in filter(lambda item: item in const.ITEMS, self.items)]
        return ", ".join(itemName)