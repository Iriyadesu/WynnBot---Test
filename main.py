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


# ---------- commands ----------


# Handling command errors
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

# Making commands case insensitive
@bot.event
async def on_message(message):
    temp = message.content.split(" ")
    message.content = str(temp[0].lower())
    for x in temp[1:]:
        message.content += " " + str(x)

    await bot.process_commands(message)


# Giving out Guest role when user joins
@bot.event
async def on_member_join(member):
    try:
        await member.add_roles(discord.utils.get(member.guild.roles, name='guest')) 
    except Exception as e:
        await print('Cannot assign role. Error: ' + str(e))


# ---------- registering commands ----------
extensions = ['Cogs.Moderation', 'Cogs.Wynncraft']

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

def setup(bot):
    bot.add_cog(Moderation(bot))