# bot.py
import os
import random
import requests
from discord.ext import commands
import discord
from dotenv import load_dotenv
###########IMPORTS###########


#! Handling discord TOKEN and PREFIX

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

####################################



@bot.event #* Handling command errors
async def on_command_error(ctx, error):
    

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")


@bot.event #* Making commands case insensitive
async def on_message(message):
    temp = message.content.split(" ")
    message.content = str(temp[0].lower())
    for x in temp[1:]:
        message.content += " " + str(x)

    await bot.process_commands(message)


@bot.command(help="Bans someone.") #! Need to add reason as optional arg
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):

        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)


@bot.command(help="Kicks someone.") #! Need to add reason as optional arg
@commands.has_permissions(ban_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        ban = discord.Embed(title=f":boom: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)




@bot.command(help="Let's you view a player's profile.") #? Need to make it look better
async def profile(ctx, PlayerName):

    r = requests.get(f'https://api.wynncraft.com/v2/player/{PlayerName}/stats')
    #get the data
    json = r.json()
    #Print the data
    if json['code'] == 400:
        return await ctx.channel.send('Cannot find user.') 
    highestlvl = 0
    for x in json['data'][0]['classes']:
        if x['professions']['combat']['level'] > highestlvl:
            highestlvl = x['professions']['combat']['level']
    embedVar = discord.Embed(title=f"{PlayerName}'s profile", color=0x00ff00)
    embedVar.add_field(name="UserName: ", value=f"{json['data'][0]['username']}", inline=True)
    embedVar.add_field(name="Rank: ", value=f"{json['data'][0]['meta']['tag']['value']}", inline=False)
    embedVar.add_field(name="Online: ", value=f"{json['data'][0]['meta']['location']['online']}", inline=True)
    embedVar.add_field(name="Server: ", value=f"{json['data'][0]['meta']['location']['server']}", inline=True)
    embedVar.add_field(name = chr(173), value = chr(173))
    embedVar.add_field(name="Guild's name: ", value=f"{json['data'][0]['guild']['name']}", inline=True)
    embedVar.add_field(name="Rank in guild: ", value=f"{json['data'][0]['guild']['rank']}", inline=True)
    embedVar.add_field(name="Playtime: ", value=f"{int((json['data'][0]['meta']['playtime'] *4.7)/60)} hours.", inline=False)
    embedVar.add_field(name="Highest Level: ", value=f"{highestlvl}", inline=False)
    embedVar.add_field(name="Joined: ", value=f"{json['data'][0]['meta']['firstJoin'][:10]}", inline=True)
    await ctx.channel.send(embed=embedVar)
    # await ctx.send(json['data'][0]['rank'])

@bot.command(help="Let's you view a guild's info.") #? Need to make it look better
async def guild(ctx, GuildName):

    r = requests.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={GuildName}')

    json = r.json()

    if "error" in json:
        return await ctx.channel.send('Cannot find guild.') 

    embedVar = discord.Embed(title=f"{GuildName}", color=0xFF0000)
    embedVar.add_field(name="Name: ", value=f"{json['name']}", inline=False)
    embedVar.add_field(name="Prefix: ", value=f"{json['prefix']}", inline=False)
    embedVar.add_field(name="Level: ", value=f"{json['level']}", inline=False)
    embedVar.add_field(name="Members: ", value=f"{len(json['members'])}", inline=False)
    embedVar.add_field(name="Territories: ", value=f"{json['territories']}", inline=False)
    # embedVar.add_field(name="Playtime: ", value=f"{json['data'][0]['meta']['playtime'] /60} hours.", inline=False)
    embedVar.add_field(name="Created at: ", value=f"{json['createdFriendly']}", inline=False)
    await ctx.channel.send(embed=embedVar)



@bot.command(help="Shows you the stats of an item.") #! Need to finish this
async def item(ctx, ItemName):
    r = requests.get(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={ItemName}')
    json = r.json()

    




bot.run(TOKEN)