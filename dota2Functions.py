import dota2apiOpenDota as oda
from classes.player import Player
import loadConstant as const
import discord
import constant.color as cl
import asyncio
from classes.dota import Dotaplayer, Match
from steam_id_converter import Convert
import CustomExceptions as ce


URL = "https://api.opendota.com/api/"
heroesList = []

ranks = {
  "1": "Herald",
  "2": "Guardian",
  "3": "Crusader",
  "4": "Archon",
  "5": "Legend",
  "6": "Ancient",
  "7": "Divine"}

TAB = "\u200B "*4
sep = f"{TAB}|{TAB}"

def GetItemNameFromId(itemId):
  if itemId in const.ITEMS:
    return const.ITEMS[itemId].dname
  return ""

def IsAccountPublicOrValid(playerId: int) -> bool:
  player = oda.GetPlayerStats(playerId)
  return "profile" in player


def ConvertPlayerID(playerId: int):
  try:
    return Convert(playerId).steam_id32_converter()
  except:
    raise ce.PlayerIDInvalid(playerId)


# For basic Player Data
def GetPlayerDataMessage(playerId: int):
  data = oda.GetPlayerStats(playerId)
  winLoseData = oda.GetPlayerOverallWinLose(playerId)
  winPercentage = str((winLoseData.win * 100) // (winLoseData.win + winLoseData.lose)) + "%"
  player = Player(data)
  displayDict = [
    {"key":"MMR", "value": player.competitiveRank},
    {"key":"Rank", "value": player.rankTier},
    {"key":"Total Wins", "value": winLoseData.win},
    {"key":"Total loss", "value": winLoseData.lose},
    {"key":"Win Percentage", "value": winPercentage}]
  # msg = ""

  em = discord.Embed(title=player.personaName)\
  .set_thumbnail(url= player.avatar)
  for index in range(len(displayDict)):
    em.add_field(name=str(displayDict[index]['key']) + ":", value=str(displayDict[index]["value"])+TAB, inline=True)
    # msg += f"**{displayDict[index]['key']}**:{TAB}{displayDict[index]['value']}{TAB}{TAB}"
    # if index % 2 != 0:
    #   em.add_field(name="\u200B", value=msg, inline=False)
    #   msg = ""

  return em

# For  Player Winlose details (currently deprecated)
def GetPlayerWinLoseMessage(playerId: int):
  data = oda.GetPlayerOverallWinLose(playerId)
  winPercentage = (data.win * 100) // (data.win + data.lose)
  message = f"Total Wins- {data.win}\nTotal loss- {data.lose}\nWin Percentage- {winPercentage}%"
  return message

# For  Player Last match Full match details
def GetPlayerLastMatchFullDetails(playerId: int):
  data = oda.GetPlayerRecentMatch(playerId)[0]
  print(data)
  return GetMatchDetails(data["match_id"])

# For  Player Last match Full match details
def GetPlayerRecentMatchMessage(playerId: int):
  playerData = oda.GetPlayerStats(playerId)
  player = Player(playerData)
  matchData = oda.GetPlayerRecentMatch(playerId)

  em = discord.Embed(title=player.personaName)\
  .set_thumbnail(url= player.avatar)

  for match in matchData:
    isRadiant = match.player_slot < 128
    victory = match.radiant_win and isRadiant
    status = "Victory" if victory else"Defeat"
    KDA = f"{match.kills}/{match.deaths}/{match.assists}"
    gameMode = const.GAME_MODE[str(match.game_mode)]["showName"]
    hero = const.HEROES[match.hero_id].localized_name
    msg = f"Match Id-{match.match_id}{TAB}{TAB}{status}{TAB}{TAB}{KDA}"
    em.add_field(name=f"Hero:{hero}", value = msg, inline=False)

  return em


# For  Player Last match details
def GetPlayerLastMatchMessage(playerId: int):
  data = oda.GetPlayerRecentMatch(playerId)[0]
  isRadiant = data.player_slot < 128
  victory = data.radiant_win and isRadiant
  status = "Victory" if victory else"Defeat"
  lobbyType = const.LOBBY_TYPE[str(data.lobby_type)]["showName"]
  gameMode = const.GAME_MODE[str(data.game_mode)]["showName"]
  KDA = f"{data.kills}/{data.deaths}/{data.assists}"
  displayDict = [
    {"key":"Status", "value": status},
    {"key":"Duration", "value": f"{data.duration // 60}min"},
    {"key":"Side", "value": f"{'Radiant' if isRadiant else 'Dire'}"},
    {"key":"Hero", "value": const.HEROES[data.hero_id].localized_name},
    {"key":"K/D/A", "value": KDA},
    {"key":"GPM", "value": data.gold_per_min},
    {"key":"XPM", "value": data.xp_per_min},
    {"key":"Last Hits", "value": data.last_hits},
    {"key":"Hero Damage", "value": data.hero_damage},
    {"key":"Tower Damage", "value": data.tower_damage},
    {"key":"Type", "value": lobbyType +" "+gameMode},
    {"key":"Party Size", "value": data.party_size}]

  em = discord.Embed(title=f"Match Id- {data.match_id}", color=cl.GREEN if victory else cl.RED)\
  .set_thumbnail(url= "http://cdn.dota2.com"+const.HEROES[data.hero_id].img)
  for index in range(len(displayDict)):
    em.add_field(name=str(displayDict[index]['key']) + ":", value=str(displayDict[index]["value"])+TAB, inline=True)
  return em


# Get Match Details
def GetMatchDetails(matchId: int):
  print(matchId)
  match = Match(oda.GetMatchDetails(matchId))
  status = "Radiant Victory" if match.radiant_win else "Dire Victory"
  title = f"Match Id- {match.match_id}\n{status}{TAB}{TAB}{match.duration // 60}min"

  playerData = [GenerateEachPlayerMatchData(player) for player in match.players]
  emTitle = discord.Embed(title=title)
  emRadiant = discord.Embed(title=f"Radiant{TAB}{TAB}Kills: {match.radiant_score}", color=cl.GREEN)
  emDire = discord.Embed(title=f"Dire{TAB}{TAB}Kills: {match.dire_score}", color=cl.RED)
  for index in range(len(playerData)):
    if index < len(playerData)//2:
      emRadiant.add_field(name=match.players[index].personaname, value = playerData[index], inline=False)
    else:
      emDire.add_field(name=match.players[index].personaname, value = playerData[index], inline=False)
  return emTitle, emRadiant, emDire


def GenerateEachPlayerMatchData(player):
  K_D_A = f"{player.kills}/{player.deaths}/{player.assists}"
  KDA = round((player.kills + player.assists) / (player.deaths or 1), 2)
  msg = ""
  # msg += f"Player Name: {player.personaname}"
  msg += f"Hero: {const.HEROES[player.hero_id].localized_name}{TAB}{K_D_A}{TAB}KDA: {KDA}\n"
  msg += f"Net Worth: {player.net_worth}{TAB}XPM: {player.xp_per_min}{TAB}GPM: {player.gold_per_min}\n"
  msg += f"Last Hits/Denies: {player.last_hits}/{player.denies}\n"
  msg += f"Damage: {player.hero_damage}{TAB}Buildings: {player.tower_damage}{TAB}Heal: {player.hero_healing}\n"
  msg += f"Items: {player.GetPlayerItemNames()}"
  return "```"+msg+"```"
