from discord.ext import commands
import discord
import requests as req
import bot_data as bd

from Wrappers.player import Player
from Wrappers.territory import Territory


class Wynncraft(commands.Cog):  # TODO: Add proper documentation to the class + methods
    def __init__(self, bot):
        self.bot = bot

    # ----- player stats -----
    @commands.command(description="Search for players")  # TODO: Need to make it look better
    async def player(self, ctx, player_name, stat=None):
        """
        Send embed with info on requested player.
        Sends specific stat if requested
        :param ctx: channel where the command was used
        :param player_name: name of the requested player
        :param stat: stat requested; default None
        :return: None
        """
        """
        # TODO: prepared for binding
        if isinstance(player_name, discord.Member):
            await ctx.channel.send(str(player_name) + ' ' + player_name)
        else:
            await ctx.channel.send('No name ' + player_name + ' ' + player_name)
        """

        player = Player(player_name)
        if not player.found:
            await ctx.channel.send(embed=bd.error_embed('API error', description='Requested player not found.'))
            return

        if stat is not None:
            try:
                player_embed = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
                player_embed.add_field(name=stat, value=player[stat])
                await ctx.channel.send(embed=player_embed)
            except:  # TODO: get type of raised exception
                await ctx.channel.send(embed=bd.error_embed('API error', description='Requested stat not found.'))
            return

        # ----- create the embed -----
        player_embed = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
        player_embed.add_field(name="UserName: ", value=player['username'], inline=True)
        player_embed.add_field(name=chr(173), value=chr(173))
        player_embed.add_field(name="Rank: ", value=player['rank'], inline=False)
        player_embed.add_field(name="Online: ", value=player['location'] if player['location'] else 'no', inline=True)
        player_embed.add_field(name=chr(173), value=chr(173))
        player_embed.add_field(name="Guild name: ", value=player['guild name'] if player['guild name'] else 'none', inline=True)
        player_embed.add_field(name="Guild rank: ", value=player['guild rank'].lower() if player['guild rank'] else 'none',
                               inline=True)
        player_embed.add_field(name="Guild prefix: ", value=player['guild instance']['prefix'], inline=True)
        player_embed.add_field(name="Playtime: ", value=f"{player['total playtime']} hours", inline=False)
        player_embed.add_field(name="Highest Level: ", value=player['highest level combat'], inline=False)
        player_embed.add_field(name="Joined: ", value=player['first join'][:10], inline=True)
        await ctx.channel.send(embed=player_embed)  # send the embed
    
    #  ----- guild stats -----
    @commands.command(description="Let's you search for guilds.")  # TODO: Need to make it look better
    async def guild(self, ctx, guild_name):
        """
        Send embed with info on requested guild.
        :param ctx: channel where the command was used
        :param guild_name: name of the requested player
        :return: None
        """
        # TODO: Create the API wrapper
        resp = req.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={guild_name}')

        data = resp.json()

        if "error" in data:
            await ctx.channel.send(embed=bd.error_embed('API error', description='Requested guild not found.'))
            return

        # ----- create the embed -----
        guild_embed = discord.Embed(title=guild_name, color=0xFF0000)
        guild_embed.add_field(name="Name: ", value=data['name'], inline=False)
        guild_embed.add_field(name="Prefix: ", value=data['prefix'], inline=False)
        guild_embed.add_field(name="Level: ", value=data['level'], inline=False)
        guild_embed.add_field(name="Members: ", value=str(len(data['members'])), inline=False)
        guild_embed.add_field(name="Territories: ", value=data['territories'], inline=False)
        # embedVar.add_field(name="Playtime: ", value=f"{json['data'][0]['meta']['playtime'] /60} hours.", inline=False)
        guild_embed.add_field(name="Created at: ", value=data['createdFriendly'], inline=False)
        await ctx.channel.send(embed=guild_embed)  # send the embed

    #  ----- territory stats -----
    @commands.command(description='Sends info about requested guild\nUse `\"name\"` for more-word names.')
    async def territory(self, ctx, territory_name):
        """
        Send embed with info on requested territory.
        :param ctx: channel where the command was used
        :param territory_name: name of the requested player
        :return: None
        """
        terr = Territory(territory_name)
        if not terr.found:
            await ctx.channel.send(embed=bd.error_embed('API error', 'Requested territory not found.'))
            return

        # ----- create the embed -----
        territory_embed = discord.Embed(title=territory_name, color=0x00FF00)
        territory_embed.add_field(name='Name:', value=territory_name)
        territory_embed.add_field(name='Owner:', value=terr['owner'])
        territory_embed.add_field(name=chr(173), value=chr(173))
        territory_embed.add_field(name='Start coords:', value=f'{terr["location"]["startX"]} {terr["location"]["startZ"]}')
        territory_embed.add_field(name='End coords:', value=f'{terr["location"]["endX"]} {terr["location"]["endZ"]}')

        await ctx.channel.send(embed=territory_embed)

    #  ----- item stats -----
    @commands.command(description="Search for items")  # TODO: Need to finish this
    async def item(self, ctx, item_name):
        # resp = req.get(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={item_name}')
        # data = resp.json()
        ctx.channel.send('Command not implemented')
        raise NotImplementedError('Command not implemented')


def setup(bot):
    bot.add_cog(Wynncraft(bot))
