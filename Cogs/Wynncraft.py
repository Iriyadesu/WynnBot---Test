from typing import Union

import discord
from discord.ext import commands

import bot_data as bd
import util
from Wrappers.player import player
from Wrappers.guild import guild
from Wrappers.territory import territory
from Wrappers.network import player_sum, players_on_worlds

try:
    from Cogs.Binder import get_binds
except ImportError:
    def get_binds() -> None:
        """Dummy function in case Binder is not loaded"""
        return None


class Wynncraft(commands.Cog):
    """
    This Cog contains command related to wynncraft.
    """
    description_ = 'Wynncraft-related commands'

    def __init__(self, bot: discord.ext.commands.Bot):
        """Used to allow to use the bot instance in the code"""
        self.bot = bot

    # ----- player stats -----
    @commands.command(usage="profile <player name>",
                      description="provides info on requested player")
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
            binds = get_binds()
            if binds is None:  # if binder was not imported
                await ctx.send(embed=util.error_embed('Binding not supported'))
                return

            if str(player_name.id) in binds:  # if the player is bound
                player_name = binds[str(player_name.id)]
            else:
                player_name = 'a'  # this name can't exist -> automatic fail

        async with ctx.typing():  # make it do something while it gets the info
            player_data = player(player_name)  # get the info

        if player_data is None:  # if the player doesn't exist send error
            await ctx.send(embed=util.error_embed('Requested player not found.'))
            return

        # ----- create the embed -----
        embed = discord.Embed(title=f"{player_name}'s profile", color=bd.embed_colors['normal'])
        embed.add_field(name="UserName: ", value=player_data['username'])
        embed.add_field(name="Rank: ", value=str(player_data['rank']) + (', veteran' if player_data['veteran'] else ''))
        if player_data['position'] != 'Player':  # if the player is offline
            embed.add_field(name="Position:", value=player_data['position'])
        if player_data['guild']['name'] is not None:
            embed.add_field(name="Guild:",
                            value=f'{player_data["guild"]["name"]} ({player_data["guild"]["rank"].lower()})')
        embed.add_field(name="Highest Level:", value=player_data['highestLvlCombat'])
        embed.add_field(name="Online: ", value=player_data['location'] if player_data['location'] else 'no')
        embed.add_field(name="Playtime:", value=f"{player_data['playtime']} hours", inline=False)
        embed.add_field(name="Joined:", value=player_data['firstJoin'][:10])

        await ctx.send(embed=embed)  # send the embed
    
    #  ----- guild stats -----
    @commands.command(usage="guild <guild name>",
                      description="provides info on requested guild")
    async def guild(self, ctx: commands.Context, guild_name):
        """
        Send embed with info on requested guild.
        :param ctx: channel where the command was used
        :param guild_name: name of the requested player
        :return: None
        """

        async with ctx.typing():
            guild_data = guild(guild_name)

        if guild_data is None:
            await ctx.send(embed=util.error_embed('Requested guild not found.'))
            return

        # ----- create the embed -----
        embed = discord.Embed(title=guild_name, color=bd.embed_colors['normal'])
        embed.add_field(name="Name: ", value=guild_data['name'], inline=True)
        embed.add_field(name="Prefix: ", value=guild_data['prefix'], inline=True)
        embed.add_field(name="Level: ", value=f'lv.{guild_data["level"]}, xp: {guild_data["xp"]}%', inline=True)
        embed.add_field(name="Members: ", value=str(len(guild_data['members'])), inline=True)
        embed.add_field(name="Territories: ", value=guild_data['territories'], inline=True)
        embed.add_field(name="Created at: ", value=guild_data['createdFriendly'], inline=False)

        await ctx.send(embed=embed)  # send the embed

    #  ----- territory stats -----
    @commands.command(usage="territory <territory name>",
                      description='provides info on requested territory')
    async def territory(self, ctx: commands.Context, *territory_name):
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
            await ctx.send(embed=util.error_embed('Requested territory not found.'
                                                  '\nPlease check capitalisation'))
            return

        # ----- create the embed -----
        embed = discord.Embed(title=territory_name, color=0x00FF00)
        embed.add_field(name='Name:', value=territory_name)
        embed.add_field(name='Owner:', value=territory_data['guild'])
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name='Start coords:',
                        value=f'{territory_data["location"]["startX"]} {territory_data["location"]["startY"]}'
                        )
        embed.add_field(name='End coords:',
                        value=f'{territory_data["location"]["endX"]} {territory_data["location"]["endY"]}')

        await ctx.send(embed=embed)

    #  ----- sum of all online players -----
    # Waiting for 1.20 API update
    @commands.command(usage="network <sum|world|find> [name]",
                      description="network stuff ig")
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

        if action == 'sum':  # sum of all players
            embed = discord.Embed(color=bd.embed_colors['normal'])
            # noinspection PyTypeChecker
            embed.add_field(name='Online players:', value=player_sum())  # doesn't actually rise an error, works fine
            await ctx.send(embed=embed)

        elif action == 'worlds':  # all worlds and their player count
            embed = discord.Embed(color=bd.embed_colors['normal'])
            world_dict = players_on_worlds()
            for world in world_dict:
                # noinspection PyTypeChecker
                embed.add_field(name=f'{world}:', value=len(world_dict[world]))
            await ctx.send(embed=embed)

        elif action == 'find':  # find a player
            if name == '':
                await ctx.send(embed=util.error_embed(f'Argument error', 'Not enough parameters passed'))
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
                embed.add_field(name='Failure', value=f'Player \"{name}\" not found')
                await ctx.send(embed=embed)

        else:
            raise util.UnknownArgumentException('Unknown parameter passed')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Wynncraft(bot))
