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
    datefmt='%I:%M:%S-%m/%d/%Y')

name = dt.datetime.utcnow().strftime('%H:%M:%S-%m/%d/%Y')


# ----- Handling discord TOKEN and PREFIX -----
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
    finally:
        l.info('Old log was moved and renamed as \'%s\'', name)
        os.rename('bot.log', name)
        shutil.move(name, './logs')
