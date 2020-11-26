# bot.py
# ---------- IMPORTS ----------
import os
import shutil
import random as rnd
import logging as l
import requests as req
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ---------- logging init ----------

# logging config
l.basicConfig(level=l.DEBUG, filename='bot.log',
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%I:%M:%S-%m/%d/%Y')

# ----- Handling discord TOKEN and PREFIX -----

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ---------- registering commands ----------
extensions = ['Cogs.Moderation', 'Cogs.Wynncraft', 'Cogs.Events']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)


# ---------- run the bot ----------
try:
    bot.run(TOKEN)
except: pass
finally:
    l.info('Old log was moved and renamed as \'%s\'', name)
    os.rename('bot.log', name)
    shutil.move(name, './logs')

