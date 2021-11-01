import os
import functions as fn
import random
import discord
import dota2apiOpenDota as d2a
from discord.ext import commands
from discord import ChannelType
import constant.constant as const
from dotenv import load_dotenv
import dota2Functions as d2func
from beautifultable import BeautifulTable
import classes.logs as logs
import CustomExceptions as ce
import databaseFunctions as dbFunc

os.system("cls" if os.name == "nt" else "clear")

# setting global variables
# mongo_setup.global_init()
load_dotenv(".env")
bot = commands.Bot(command_prefix="!")
DISCORD_TOKEN = os.getenv("TOKEN_DISCORD")

# Event Started
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if str(message.author) in const.ignore_user:
    await message.channel.send(random.choice(const.stop_chat))

  await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(random.choice(const.missing_argument))
  elif isinstance(error, commands.MemberNotFound):
    await ctx.send("Naam Barbar Daal") 
  elif isinstance(error, ce.PlayerIDInvalid) or isinstance(error, ce.MatchIdNotFound) or isinstance(error, ce.PlayerIdNotFound):
    await ctx.send(error.message)
  else:
    # logs.logError(error)
    raise error
# Event Ends

# Commands Started
@bot.command(name="hello")
async def hello_cmd(ctx):
  print (ctx.author)
  await ctx.send(f" Hello {fn.GetNickName(str(ctx.author))} {ctx.author}.")

@bot.command(name="chup")
async def mute_cmd(ctx, usr: discord.Member):
  await usr.edit(mute=True)
  await ctx.send(f"{usr.mention} ko chup kr diya.")

@bot.command(name="bol")
async def unmute_cmd(ctx, usr: discord.Member):
  await usr.edit(mute=False)
  await ctx.send(f"{usr.mention} fhir bolne laga.")

@bot.command(name="sun_mat")
async def deafean_cmd(ctx, usr: discord.Member):
  await usr.edit(deafen=True)
  await ctx.send(f"{usr.mention} ko behera kr diya.")

@bot.command(name="sun")
async def undeafean_cmd(ctx, usr: discord.Member):
  await usr.edit(deafen=False)
  await ctx.send(f"{usr.mention} fhir sunne laga.")

@bot.command(name="nikal")
async def remove_channel_cmd(ctx, usr: discord.Member):
  await usr.edit(voice_channel=None)
  await ctx.send(f"{usr.mention} ko nikal diya.") 

@bot.command(name="aaja")
async def add_channel_cmd(ctx, usr: discord.Member, chl: str):
  for channel in ctx.guild.voice_channels:
    if channel.type == ChannelType.voice and channel.name == chl:
      print(usr.voice == None)
      if usr.voice == None:
        await ctx.send(f"{usr.mention} ko phele kisi channel me aane ko bol.") 
      else:
        await usr.edit(voice_channel=channel)
        await ctx.send(f"{usr.mention} ko {chl} me daal diya.") 
      return
  await ctx.send("Channel ka naam barabar nhi hai") 

# Commands Ends

# Add DB commands

@bot.command(name="add_Steam_Id")
async def get_dota2_player_recent_matches(ctx, usr: str, playerId: str):
  res = dbFunc.AddPlayer(fn.getOnlyId(usr), str(playerId))
  await ctx.send("Linked Successfully" if res else "Already Added") 

# Add DB commands End

#Dota 2 command Start

@bot.command(name="heroes")
async def get_dota2_heros(ctx):
  a = d2a.GetAllHeros()
  print(a)
  await ctx.send(a[0])

@bot.command(name="player")
async def get_dota2_player(ctx, player: str):
  if fn.isInstanceDiscordId(player):
    playerId = dbFunc.GetPlayerSteamId(fn.getOnlyId(player))
    if playerId is None:
      await ctx.send("No Steam Id Linked to this member.") 
      return
  else:
    playerId = player
  playerId32 = d2func.ConvertPlayerID(playerId)
  em = d2func.GetPlayerDataMessage(playerId32)
  await ctx.channel.send(embed=em)

@bot.command(name="last_match")
async def get_dota2_player_last_match(ctx, player: str):
  if fn.isInstanceDiscordId(player):
    playerId = dbFunc.GetPlayerSteamId(fn.getOnlyId(player))
    if playerId is None:
      await ctx.send("No Steam Id Linked to this member.") 
      return
  else:
    playerId = player
  playerId32 = d2func.ConvertPlayerID(playerId)
  em = d2func.GetPlayerLastMatchMessage(playerId32)
  await ctx.channel.send(embed=em)

@bot.command(name="match")
async def get_match_details(ctx, matchId: str):
  emTitle, emRadiant, emDire = d2func.GetMatchDetails(matchId)
  await ctx.channel.send(embed=emTitle)
  await ctx.channel.send(embed=emRadiant)
  await ctx.channel.send(embed=emDire)

@bot.command(name="last_match_details")
async def get_dota2_player_last_match_details(ctx, player: str):
  if fn.isInstanceDiscordId(player):
    playerId = dbFunc.GetPlayerSteamId(fn.getOnlyId(player))
    if playerId is None:
      await ctx.send("No Steam Id Linked to this member.") 
      return
  else:
    playerId = player
  playerId32 = d2func.ConvertPlayerID(playerId)
  emTitle, emRadiant, emDire = d2func.GetPlayerLastMatchFullDetails(playerId32)
  await ctx.channel.send(embed=emTitle)
  await ctx.channel.send(embed=emRadiant)
  await ctx.channel.send(embed=emDire)

@bot.command(name="recent_match")
async def get_dota2_player_recent_matches(ctx, playerId: str):
  playerId32 = d2func.ConvertPlayerID(playerId)
  em = d2func.GetPlayerRecentMatchMessage(playerId32)
  await ctx.channel.send(embed=em)

@bot.command(name="test")
async def get_dota2_player_last_match_test(ctx, usr):
  print(ctx.author.id)
  print(ctx.guild.id)
  for i in bot.guilds:
    print(i)
  usr = bot.guilds[ctx.guild.id].get_member(ctx.author.id)
  print(type(usr))
  print(usr)
  await ctx.channel.send(usr)

#Dota 2 Command Ends



bot.run(DISCORD_TOKEN)