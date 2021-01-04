from typing import Union

from discord.ext import commands
import discord
import requests as req

import bot_data as bd
from Wrappers.player import player
from Wrappers.guild import guild
from Wrappers.territory import Territory
from Cogs.Binder import Binder


class Wynncraft(commands.Cog):  # TODO: Add proper documentation to the class + methods
    def __init__(self, bot):
        self.bot = bot

    # ----- player stats -----
    @commands.command(description="provides info on requested player", usage="!profile <player name>")  # TODO: Need to make it look better
    async def player(self, ctx: commands.Context, player_name: Union[discord.Member, str], stat=None):
        """
        Send embed with info on requested player.
        Sends specific stat if requested

        :param ctx: channel where the command was used
        :param player_name: name of the requested player
        :param stat: stat requested; default None
        :return: None
        """

        # ----- bind support -----
        if isinstance(player_name, discord.Member):  # if a discord member was used
            await ctx.channel.send('Bind is not yet fully supported')

            player_name = Binder.get_binds()[player_name.id]

        async with ctx.typing():  # make it do something while it gets the info
            player_data = player(player_name)  # get the info

        if player_data is None:  # if the player doesn't exist send error
            await ctx.channel.send(embed=bd.error_embed('API error', description='Requested player not found.'))
            return

        if stat is not None:  # if stats was provided
            try:
                player_embed = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
                player_embed.add_field(name=stat, value=player_data[stat])
                await ctx.channel.send(embed=player_embed)
            except KeyError:  # if stats was not found
                await ctx.channel.send(embed=bd.error_embed('API error', description='Requested stat not found.'))
            return

        # ----- create the embed -----
        player_embed = discord.Embed(title=f"{player_name}'s profile", color=0x00ff00)
        player_embed.add_field(name="UserName: ", value=player_data['username'], inline=True)
        player_embed.add_field(name=chr(173), value=chr(173))
        player_embed.add_field(name="Rank: ", value=player_data['rank'], inline=False)
        player_embed.add_field(name="Online: ", value=player_data['location'] if player_data['location'] else 'no', inline=True)
        player_embed.add_field(name=chr(173), value=chr(173))
        player_embed.add_field(name="Guild name: ",
                               value=player_data['guild name'] if player_data['guild name'] else 'none', inline=True)
        player_embed.add_field(name="Guild rank: ",
                               value=player_data['guild rank'].lower() if player_data['guild rank'] else 'none',
                               inline=True)
        player_embed.add_field(name="Guild prefix: ", value=player_data['guild instance']['prefix'], inline=True)
        player_embed.add_field(name="Playtime: ", value=f"{player_data['total playtime']} hours", inline=False)
        player_embed.add_field(name="Highest Level: ", value=player_data['highest level combat'], inline=False)
        player_embed.add_field(name="Joined: ", value=player_data['first join'][:10], inline=True)
        await ctx.channel.send(embed=player_embed)  # send the embed
    
    #  ----- guild stats -----
    @commands.command(description="provides info on requested guild", usage="!guild <guild name>")  # TODO: Need to make it look better
    async def guild(self, ctx: commands.Context, guild_name):
        """
        Send embed with info on requested guild.
        :param ctx: channel where the command was used
        :param guild_name: name of the requested player
        :return: None
        """
        # TODO: Create the API wrapper
        async with ctx.typing():
            guild_data = guild(guild_name)

        if "error" in guild_data:
            await ctx.channel.send(embed=bd.error_embed('API error', description='Requested guild not found.'))
            return

        # ----- create the embed -----
        guild_embed = discord.Embed(title=guild_name, color=0xFF0000)
        guild_embed.add_field(name="Name: ", value=guild_data['name'], inline=False)
        guild_embed.add_field(name="Prefix: ", value=guild_data['prefix'], inline=False)
        guild_embed.add_field(name="Level: ", value=guild_data['level'], inline=False)
        guild_embed.add_field(name="Members: ", value=str(len(guild_data['members'])), inline=False)
        guild_embed.add_field(name="Territories: ", value=guild_data['territories'], inline=False)
        guild_embed.add_field(name="Created at: ", value=guild_data['created friendly'], inline=False)

        await ctx.channel.send(embed=guild_embed)  # send the embed

    #  ----- territory stats -----
    @commands.command(description='provides info on requested territory', usage="!territory <territory name>")
    async def territory(self, ctx: commands.Context, territory_name):
        """
        Send embed with info on requested territory.
        :param ctx: channel where the command was used
        :param territory_name: name of the requested player
        :return: None
        """
        async with ctx.typing():
            terr = Territory(territory_name)
        if not terr.found:
            await ctx.channel.send(embed=bd.error_embed('API error', description='Requested territory not found.'))
            return

        # ----- create the embed -----
        territory_embed = discord.Embed(title=territory_name, color=0x00FF00)
        territory_embed.add_field(name='Name:', value=territory_name)
        territory_embed.add_field(name='Owner:', value=terr['owner'])
        territory_embed.add_field(name=chr(173), value=chr(173))
        territory_embed.add_field(name='Start coords:',
                                  value=f'{terr["location"]["startX"]} {terr["location"]["startZ"]}')
        territory_embed.add_field(name='End coords:', value=f'{terr["location"]["endX"]} {terr["location"]["endZ"]}')

        await ctx.channel.send(embed=territory_embed)

    #  ----- item stats -----
    @commands.command(description="provides info on requested item\n**~~__note__:**: put more word names between double quotes `\"`", usage="!item <item name>")  # TODO: Need to implement this
    async def item(self, ctx: commands.Context, item_name: str):  # TODO: Create a wrapper
        """
        Raises NotImplemented error
        """
        """
        async with ctx.typing():
            resp = req.get(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={item_name}')
            data = resp.json()
            pass
        """
        ctx.channel.send('Command not implemented')
        raise NotImplementedError('Command not implemented')


def setup(bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Wynncraft(bot))
