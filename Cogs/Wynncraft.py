from discord.ext import commands
import discord
import requests as req

from Wrappers.player import Player


class Wynncraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- player stats -----
    @commands.command(description="Search for players") # Need to make it look better
    async def profile(self, ctx, player_name, stat=None):
        player = Player(player_name)

        if stat is not None:
            try:
                embedVar = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
                embedVar.add_field(name=stat, value=player[stat])
                await ctx.channel.send(embed=embedVar)
                return
            except:
                await ctx.channel.send('requested stat was not found')
                return

        embedVar = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
        embedVar.add_field(name="UserName: ", value=f"{player['username']}", inline=True)
        embedVar.add_field(name=chr(173), value=chr(173))
        embedVar.add_field(name="Rank: ", value=f"{player['rank']}", inline=False)
        embedVar.add_field(name="Online: ", value=f"{player['location']}", inline=True)
        embedVar.add_field(name=chr(173), value=chr(173))
        embedVar.add_field(name="Guild name: ", value=f"{player['guild name']}", inline=True)
        embedVar.add_field(name="Guild rank: ", value=f"{player['guild rank'].lower() if player['guild rank'] else 'none'}",
                           inline=True)
        embedVar.add_field(name="Playtime: ", value=f"{player['total playtime']} hours.", inline=False)
        embedVar.add_field(name="Highest Level: ", value=f"{player['highest level combat']}", inline=False)
        embedVar.add_field(name="Joined: ", value=f"{player['first join'][:10]}", inline=True)
        await ctx.channel.send(embed=embedVar)
    
    #  ----- guild stats -----
    @commands.command(description="Let's you search for guilds.") #? Need to make it look better
    async def guild(self, ctx, guild_name):
        resp = req.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={guild_name}')

        data = resp.json()

        if "error" in data:
            return await ctx.channel.send('Cannot find guild.') 

        embedVar = discord.Embed(title=f"{guild_name}", color=0xFF0000)
        embedVar.add_field(name="Name: ", value=f"{data['name']}", inline=False)
        embedVar.add_field(name="Prefix: ", value=f"{data['prefix']}", inline=False)
        embedVar.add_field(name="Level: ", value=f"{data['level']}", inline=False)
        embedVar.add_field(name="Members: ", value=f"{len(data['members'])}", inline=False)
        embedVar.add_field(name="Territories: ", value=f"{data['territories']}", inline=False)
        # embedVar.add_field(name="Playtime: ", value=f"{json['data'][0]['meta']['playtime'] /60} hours.", inline=False)
        embedVar.add_field(name="Created at: ", value=f"{data['createdFriendly']}", inline=False)
        await ctx.channel.send(embed=embedVar)

    #  ----- item stats -----
    @commands.command(description="Search for items") #! Need to finish this
    async def item(self, ctx, item_name):
        resp = req.get(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={item_name}')
        data = resp.json()


def setup(bot):
    bot.add_cog(Wynncraft(bot))
