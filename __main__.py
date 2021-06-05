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
    - nothing currently
  finally:
    - rename the log file ("YYYY_M_D-_h_min_s.log" format)
    - end logging
    - move the log to the "logs" folder

Permissions required for the bot:
-   Audit log
-   Manage role  (note: they have to be apparently lower that the bot's role)
-   Kick/ban members
-   View channels
-   Send messages
-   Manage messages
-   Attack files
-   Read message history
-   Add reactions
"""
__author__ = 'TrapinchO (original and current) & FriendlyPudding (original)'
__version__ = '1.2.0'

# -------------------- To-Do --------------------
# TODO: Check all of the code
# TODO: Package-ify and module-ify
#   Done, though I think I messed up

# -------------------- IMPORTS --------------------
import datetime as dt
import logging
import os
import shutil
import sys

import discord

import util


if __name__ == '__main__':  # prevent any side effects

    config = util.load_config()

    # -------------------- logging init --------------------
    # logging config
    logging.basicConfig(level=config['logging_level'], filename='bot.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d-%H:%M:%S'
                        )

    if not os.path.exists('logs'):  # if directory "logs" does not exist
        os.mkdir('logs')
        util.log_print('Directory "logs" not found, creating it', 'WARNING')
    elif not os.path.isdir('logs'):
        # if it exists but is not a directory but a file
        # (happens when log file is moved but the directory does not exist)
        os.remove('logs')
        os.mkdir('logs')
        util.log_print('File "logs" is not a directory, removing the file and creating a directory', 'WARNING')

    # -------------------- the bot --------------------
    # ----- bot intents -----
    intents = discord.Intents.default()
    intents.members = True

    # ----- bot instance -----
    bot = util.CustomBot(command_prefix=util.determine_prefix, intents=intents, case_insensitive=True)

    # ---------- registering commands ----------
    bot.remove_command('help')  # remove the default help command

    for ext in config['enabled_extensions']:
        bot.load_extension(ext)

    # -------------------- running the script --------------------
    # ---------- Handling discord TOKEN ----------
    if len(sys.argv) > 1:  # if the patch is specified as an argument
        path = sys.argv[1]
    else:  # default path
        path = '../../discord_token.txt'

    with open(path, 'r') as file:  # get the token
        TOKEN = file.read()

    log_name = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.log'  # name of the log
    # NOTE: Time is in GMT+1 (Czech time), NOT UTC
    # ---------- run the bot ----------
    try:
        print(f'Bot script started at {dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")} on version {__version__}')
        logging.info(f'Bot script started on version {__version__}')
        bot.run(TOKEN)  # run the bot
    except Exception as e:  # something happened
        logging.error(repr(e))
        raise e
    finally:
        # ---------- cleanup ----------
        util.log_print(f'Old log was moved and renamed as \'{log_name}\'')
        logging.shutdown()  # end the logging

        os.rename('bot.log', log_name)  # rename and move log
        shutil.move(log_name, 'logs')  # if run normally
