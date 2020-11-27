from discord.ext import commands
import discord
import requests as req

class Wynncraft(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # ----- player stats
    @commands.command(description="Search for players") # Need to make it look better
    async def profile(self,ctx, PlayerName):

        r = req.get(f'https://api.wynncraft.com/v2/player/{PlayerName}/stats')
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
    
     # ----- guild stats
    @commands.command(description="Let's you search for guilds.") #? Need to make it look better
    async def guild(self,ctx, GuildName):
        r = req.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={GuildName}')

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

    # ----- item stats
    @commands.command(description="Search for items") #! Need to finish this
    async def item(self,ctx, ItemName):
        r = req.get(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={ItemName}')
        json = r.json()

def setup(bot):
    bot.add_cog(Wynncraft(bot))