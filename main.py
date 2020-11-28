# bot.py
# ---------- IMPORTS ----------
import os
import shutil
import logging as l
import datetime as dt
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ---------- logging init ----------
# logging config

l.basicConfig(level=l.INFO, filename='bot.log',
              format='%(asctime)s %(levelname)s: %(message)s',
              datefmt='%I:%M:%S-%m/%d/%Y'
              )

name = 'bot_' + dt.datetime.utcnow().strftime('%H-%M-%S_%m%d%Y') + '.log'


# ----- Handling discord TOKEN and PREFIX -----
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    with open('../hall.txt', 'r') as f:
        TOKEN = f.read()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------- registering commands ----------

bot.remove_command('help')

extensions = ['Cogs.Moderation', 'Cogs.Wynncraft', 'Cogs.Events', 'Cogs.Info']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    # ---------- run the bot ----------
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(e)
    finally:
        move_log = f'Old log was moved and renamed as \'{name}\''
        print(move_log)
        l.info(move_log)
        l.shutdown()
        os.rename('bot.log', name)
        shutil.move(name, './logs')
