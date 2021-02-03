"""
This is the main module for the bot.
It can be run several ways:
- __main__.py: just running the script
- start.bat: used because PyCharm seems to be idiotic sometimes
- running the entire package: why not

What it does:
1) imports modules
2) sets up logging
3) loads token
4) states intents (+ creates bot instance)
5) adds cogs to the bot
6) runs the bot
  try:
    - logs "Bot script started"
    - runs it
      - bot.run()
      - event "on_connect": only logs for now
      - event "on_ready": logs and sets presence
  except:
    - print the exception
  finally:
    - rename the log file ("YYYY_M_D-_h_min_s.log" format)
    - end logging
    - move the log to the "logs" folder

"""

# ---------- IMPORTS ----------
import os
import sys
import shutil
import logging
import datetime as dt
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ---------- logging init ----------
# logging config

logging.basicConfig(level=logging.INFO, filename='bot.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y/%m/%d-%H:%M!%S'
                    )

name = dt.datetime.utcnow().strftime('%Y_%m_%d-%H_%M_%S') + '.log'


# ---------- Handling discord TOKEN and PREFIX ----------
# -- FriendlyPudding's way --
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is not None:
    logging.debug('Token acquired from .env file')


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
bot.remove_command('help')  # remove default help command

extensions = ('Cogs.Moderation', 'Cogs.Wynncraft', 'Cogs.Events', 'Cogs.Info', 'Cogs.Binder')

# ---------- running the script ----------
if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    # ---------- run the bot ----------
    try:
        print('Bot script started')
        logging.info('Bot script started on version 0.5.10')
        bot.run(TOKEN)  # run the bot
    except Exception as e:  # something happened - print the exception
        print(e)
    finally:
        print(f'Old log was moved and renamed as \'{name}\'')
        logging.info(f'Old log was moved and renamed as \'{name}\'')  # log "bot.log" handling
        logging.shutdown()  # end the logging

        os.rename('bot.log', name)  # rename and move log
        shutil.move(name, './logs')  # if run normally
