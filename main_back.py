import os
import functions as fn
import random

from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!')

stop_chat = ["shut up noob", "don't talk", "chup bhet", "bot mat", "shant bas", "aapna kaam kr"]

ignore_user = [""]


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if str(message.author) in ignore_user:
    await message.channel.send(random.choice(stop_chat))

  
@bot.command(name='hello')
async def hello_cmd(message):
  print("in")
  await message.channel.send("Hello " + fn.GetNickName(str(message.author)))

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
  

bot.run(os.getenv("TOKEN"))