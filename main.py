# bot.py
# ---------- IMPORTS ----------
import os
import shutil
import logging as log
import datetime as dt
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ---------- logging init ----------
# logging config

log.basicConfig(level=log.INFO, filename='bot.log',
                format='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y_%m_%d-%H_%M_%S'
                )

name = dt.datetime.utcnow().strftime('%Y_%m_%d-%H_%M_%S') + '.log'


# ----- Handling discord TOKEN and PREFIX -----
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    with open('../token.txt', 'r') as f:
        TOKEN = f.read()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# ---------- registering commands ----------

bot.remove_command('help')

extensions = ['Cogs.Moderation', 'Cogs.Wynncraft', 'Cogs.Events', 'Cogs.Info', 'Cogs.Binder']


if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    # ---------- run the bot ----------
    try:
        log.info('Bot successfully started')
        bot.run(TOKEN)
    except Exception as e:
        print(e)
    finally:
        # move the log into "logs" folder
        move_log = f'Old log was moved and renamed as \'{name}\''
        print(move_log)
        log.info(move_log)
        log.shutdown()
        os.rename('bot.log', name)
        shutil.move(name, './logs')
