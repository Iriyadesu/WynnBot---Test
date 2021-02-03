from typing import Union

from discord.ext import commands
import discord

import bot_data as bd
from Wrappers.player import player
from Wrappers.guild import guild
from Wrappers.territory import territory
from Wrappers.network import player_sum, players_on_worlds
from Cogs.Binder import Binder


class Wynncraft(commands.Cog):
    """
    This Cog contains command related to wynncraft.

    Due to 1.20 breaking some parts of the API
    """
    def __init__(self, bot: discord.ext.commands.Bot):
        """Used to allow to use the bot instance in the code"""
        self.bot = bot

    # ----- player stats -----
    # Waiting for 1.20 API update
    @commands.command(description="provides info on requested player",
                      usage="!profile <player name>")  # TODO: Need to make it look better
    async def player(self, ctx: commands.Context, player_name: Union[discord.Member, str]):
        """
        Send embed with info on requested player.
        Sends specific stat if requested

        :param ctx: channel where the command was used
        :param player_name: name of the requested player
        :return: None
        """

        # ----- bind support -----
        if isinstance(player_name, discord.Member):  # if a discord member was used
            await ctx.send('Bind is not yet fully supported')

            player_name = Binder.get_binds()[player_name.id]

        async with ctx.typing():  # make it do something while it gets the info
            player_data = player(player_name)  # get the info

        if player_data is None:  # if the player doesn't exist send error
            await ctx.send(embed=bd.error_embed('API error', 'Requested player not found.'))
            return

        # ----- create the embed -----
        player_embed = discord.Embed(title=f"{player_name}'s profile", color=bd.embed_colors['normal'])
        player_embed.add_field(name="UserName: ", value=player_data['username'], inline=True)
        player_embed.add_field(name="Rank: ", value=player_data['rank'], inline=True)
        player_embed.add_field(name="Online: ", value=player_data['location'] if player_data['location'] else 'no',
                               inline=False)
        player_embed.add_field(name="Guild name: ",
                               value=player_data['guild']['name'] if player_data['guild']['name'] else 'none', inline=True)
        player_embed.add_field(name="Guild rank: ",
                               value=player_data['guild']['rank'].lower() if player_data['guild']['rank'] else 'none',
                               inline=True)
        player_embed.add_field(name="Playtime: ", value=f"{player_data['playtime']} hours", inline=False)
        player_embed.add_field(name="Highest Level: ", value=player_data['highestLvlCombat'], inline=False)
        player_embed.add_field(name="Joined: ", value=player_data['firstJoin'][:10], inline=True)

        await ctx.send(embed=player_embed)  # send the embed
    
    #  ----- guild stats -----
    # Waiting for 1.20 API update
    @commands.command(description="provides info on requested guild", usage="!guild <guild name>")
    async def guild(self, ctx: commands.Context, guild_name):  # TODO: Need to make it look better
        """
        Send embed with info on requested guild.
        :param ctx: channel where the command was used
        :param guild_name: name of the requested player
        :return: None
        """

        async with ctx.typing():
            guild_data = guild(guild_name)

        if guild_data is None:
            await ctx.send(embed=bd.error_embed('API error', 'Requested guild not found.'))
            return

        # ----- create the embed -----
        guild_embed = discord.Embed(title=guild_name, color=bd.embed_colors['normal'])
        guild_embed.add_field(name="Name: ", value=guild_data['name'], inline=True)
        guild_embed.add_field(name="Prefix: ", value=guild_data['prefix'], inline=True)
        guild_embed.add_field(name="Level: ", value=guild_data['level'], inline=True)
        guild_embed.add_field(name="Members: ", value=str(len(guild_data['members'])), inline=True)
        guild_embed.add_field(name="Territories: ", value=guild_data['territories'], inline=True)
        guild_embed.add_field(name="Created at: ", value=guild_data['createdFriendly'], inline=False)

        await ctx.send(embed=guild_embed)  # send the embed

    #  ----- territory stats -----
    # Waiting for 1.20 API update
    @commands.command(description='provides info on requested territory', usage="!territory <territory name>")
    async def territory(self, ctx: commands.Context, *territory_name):  # TODO: Doesn't work
        """
        Send embed with info on requested territory.
        :param ctx: channel where the command was used
        :param territory_name: name of the requested player
        :return: None
        """
        territory_name = ' '.join(territory_name)

        async with ctx.typing():
            territory_data = territory(territory_name)
        if territory_data is None:
            await ctx.send(
                embed=bd.error_embed('API error', 'Requested territory not found.\nPlease check capitalisation')
            )
            return

        # ----- create the embed -----
        territory_embed = discord.Embed(title=territory_name, color=0x00FF00)
        territory_embed.add_field(name='Name:', value=territory_name)
        territory_embed.add_field(name='Owner:', value=territory_data['guild'])
        territory_embed.add_field(name=chr(173), value=chr(173))
        territory_embed.add_field(name='Start coords:',
                                  value=f'{territory_data["location"]["startX"]} {territory_data["location"]["startY"]}'
                                  )
        territory_embed.add_field(name='End coords:',
                                  value=f'{territory_data["location"]["endX"]} {territory_data["location"]["endY"]}')

        await ctx.send(embed=territory_embed)

    #  ----- sum of all online players -----
    # Waiting for 1.20 API update
    @commands.command(description="network stuff ig", usage="!network <action> [name]")
    async def network(self, ctx: commands.Context, action: str, name: str = ''):
        """
        Get network data from Wynn API

        Capabilities:
        - get sum of all online players on Wynncraft (sum)
        - get sum of all players on each world (worlds)
        - find a world of specific player (find <name>)
        
        :param ctx: channel where the command was used
        :param action: action you want to take
        :param name: only used when using "find" action
        :return: None

        """

        if action == 'sum':
            embed = discord.Embed(color=bd.embed_colors['normal'])
            embed.add_field(name='Online players:', value=player_sum())
            await ctx.send(embed=embed)

        elif action == 'worlds':
            embed = discord.Embed(color=bd.embed_colors['normal'])
            world_dict = players_on_worlds()
            for world in world_dict:
                embed.add_field(name=world, value=len(world_dict[world]))
            await ctx.send(embed=embed)

        elif action == 'find':
            if name == '':
                await ctx.send(
                    embed=bd.error_embed(f'Argument error', 'Not enough parameters passed')
                )
                return

            world_dict = players_on_worlds()
            for world in world_dict:
                if name in world_dict[world]:
                    embed = discord.Embed(title=f'Player {name} found',
                                          color=bd.embed_colors['normal'])
                    embed.add_field(name='World:', value=world)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(color=bd.embed_colors['error'])
                embed.add_field(name='.', value=f'Player \"{name}\" not found')
                await ctx.send(embed=embed)

        else:
            await ctx.send(embed=bd.error_embed(f'Argument error', 'Unknown parameters passed'))

    #  ----- item stats -----
    @commands.command(description='Command not yet implemented', usage="!item <item name>")
    async def item(self, ctx: commands.Context, item_name: str):  # TODO: Create a wrapper or remove the command
        """
        Raises NotImplemented error
        """
        """
        from Wrappers.__init__ import api_call
        async with ctx.typing():
            resp = api_call(f'https://api.wynncraft.com/public_api.php?action=itemDB&search={item_name}')
            data = resp.json()
            pass
        """
        await ctx.send(embed=bd.error_embed('Implementation error', 'Command not implemented'))
        raise NotImplementedError('Command not implemented')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Wynncraft(bot))
