ranks = {
  "1": "Herald",
  "2": "Guardian",
  "3": "Crusader",
  "4": "Archon",
  "5": "Legend",
  "6": "Ancient",
  "7": "Divine"}


class Player:

    def __init__(self, playerData):
        profile = playerData.profile
        self.accountId = profile.account_id
        self.personaName = profile.personaname
        self.leaderboardRank = playerData.leaderboard_rank
        self.rankTierNum = str(playerData.rank_tier)
        self.competitiveRank = playerData.competitive_rank
        self.rankTier = self.GetPlayerRankTier()
        self.avatar = profile.avatar
        self.steamid = profile.steamid



    def GetPlayerRankTier(self) -> str:
        if self.rankTierNum is None:
            return None

        if self.leaderboardRank:
            return "Immortal rank {}".format(self.rankTierNum)

        if self.rankTierNum[0] == "8":
            return "Immortal"

        return "{} {}".format(ranks[self.rankTierNum[0]], self.rankTierNum[1])

  