"""
This is the main module for the bot.
It can be run several ways:
- __main__.py = just running the script
- start.bad = used because PyCharm seems to be idiotic sometimes
- running the entire folder = why not

What it does:
- import modules
- sets up logging
- loads token
- states intents (+ creates bot instance)
- adds other modules to the bot
- runs the bot
  try:
    - logs it
    - runs it
  excpet:
    - print the exception
  finally:
    - rename the log
    - end logging
    - move the log

"""

# ---------- IMPORTS ----------
import os
import sys
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


# ---------- Handling discord TOKEN and PREFIX ----------
# -- FriendlyPudding's way --
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is not None:
    log.debug('Token acquired from .env file')

# -- TrapinchO's way --
if TOKEN is None:
    if len(sys.argv) > 1:  # if the patch is specified as an argument
        with open(sys.argv[1], 'r') as f:
            TOKEN = f.read()
    else:  # if not
        with open('../discord_token.txt', 'r') as f:
            TOKEN = f.read()


# ----- bot intents -----
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


# ---------- registering commands ----------

bot.remove_command('help')

extensions = ['Cogs.Moderation', 'Cogs.Wynncraft', 'Cogs.Events', 'Cogs.Info', 'Cogs.Binder']

# ---------- running the script ----------
if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    # ---------- run the bot ----------
    try:
        print('Bot script started')
        log.info('Bot script started')
        bot.run(TOKEN)  # run the bot
    except Exception as e:  # something happened - print the exception
        print(e)
    finally:
        print(f'Old log was moved and renamed as \'{name}\'')
        log.info(f'Old log was moved and renamed as \'{name}\'')  # log "bot.log" handling
        log.shutdown()  # end the logging

        os.rename('bot.log', name)  # rename and move log
        shutil.move(name, './logs')  # if run normally
