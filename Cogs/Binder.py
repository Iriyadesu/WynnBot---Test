"""
Module for a class containing commands for binding discord user to Wynncraft account
"""
__all__ = [
    'Binder',
    'set_binds',
    'get_binds',
    'setup'
]

import json

import discord
from discord.ext import commands

import bot_data as bd
import util
from Wrappers.player import player


# TODO: Check if permission restrictions work
class Binder(commands.Cog):
    """
    Class for binding discord user to minecraft IGN through Wynncraft API
    """
    description_ = 'Commands for binding discord user to Wynncraft account'

    def __init__(self, bot: util.CustomBot):
        self.bot = bot

    @commands.command(usage="bind <create|update|delete|get> <username|.> <member>",
                      description="Command for binding a discord member to minecraft IGN")
    async def bind(self, ctx: commands.Context, action: str, username: str, member: discord.Member = None):
        """
        Command for binding discord members to minecraft IGN

        :param ctx: context of the message
        :param action: action to make
        :param username: IGN of the affected user; anything where irrelevant
        :param member: affected user
        :return: None
        """
        if member is None:
            member = ctx.author

        binds = get_binds()  # get binds

        # ---------- bind username to user
        if action.lower() == 'create':
            passed = util.check_conditions(
                (str(member.id) not in binds, f'Member {member.mention} is already bound'),
                (username not in binds.values(), f'Username \"{username}\" is already bound'),
                (player(username) is not None, f'Player name \"{username}\" does not exist'),
            )
            if passed is not True:  # if any condition failed -> send its message and return
                await ctx.channel.send(embed=util.error_embed(passed))
                return

            binds[str(member.id)] = username  # add player to the list
            set_binds(binds)  # save the new bind

            await ctx.channel.send(embed=discord.Embed(title='Success!',
                                                       description=f'Member {member.mention} was bound to \"{username}\"',
                                                       colour=bd.embed_colors['info']))
        # ---------- update IGN of a user
        elif action.lower() == 'update' and ctx.message.author.guild_permissions.administrator:
            passed = util.check_conditions(
                (str(member.id) in binds, f'Member {member.mention} not bound'),
                (player(username) is not None, f'Player name \"{username}\" does not exist'),
                (username not in binds.values(), f'Username \"{username}\" is already bound to'),
            )
            if passed is not True:  # if any condition failed -> send its message and return
                await ctx.channel.send(embed=util.error_embed(passed))
                return

            binds[str(member.id)] = username  # add player to the list
            set_binds(binds)  # save the new bind

            await ctx.channel.send(embed=discord.Embed(title='Success!',
                                                       description=f'Updated bind of {member.mention} to \"{username}\"',
                                                       colour=bd.embed_colors['info']))

        # ---------- remove IGN of a user
        elif action.lower() == 'delete' and ctx.message.author.guild_permissions.administrator:
            passed = util.check_conditions(
                (str(member.id) in binds, f'Member {member.mention} not bound'),
            )
            if passed is not True:  # if any condition failed -> send its message and return
                await ctx.channel.send(embed=util.error_embed(passed))
                return

            del binds[str(member.id)]  # remove the player from the list
            set_binds(binds)

            await ctx.channel.send(embed=discord.Embed(title='Success!',
                                                       description=f'Deleted bind of {member.mention}',
                                                       colour=bd.embed_colors['info']))

        # ---------- get IGN of a user
        elif action.lower() == 'get':  # get IGN from a user
            passed = util.check_conditions(
                (str(member.id) in binds, f'Member {member.mention} not bound')
            )
            if passed is not True:  # if any condition failed -> send its message and return
                await ctx.channel.send(embed=util.error_embed(passed))
                return

            await ctx.channel.send(embed=discord.Embed(title='Successs!',
                                                       description=f'{member.mention} is bound to \"{binds[str(member.id)]}\"',
                                                       colour=bd.embed_colors['info']))

        # ---------- invalid action
        else:
            raise util.UnknownArgumentException('Unknown parameter passed')


def get_binds() -> dict[str, str]:
    """
    Helper function for getting a dictionary of bound members' IDs and IGN

    :return: dict of user IDs and binds
    """
    with open('data/player_bind.txt', 'r') as file:
        return json.loads(file.read())  # maybe take the extra step for json?


def set_binds(binds: dict[str, str]):
    """
    Helper function for saving  a dictionary of bound members' IDs and IGN

    :param binds: binds to save
    """
    with open('data/player_bind.txt', 'w') as file:  # write it into a file
        file.write(json.dumps(binds, indent=2))


def setup(bot: util.CustomBot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Binder(bot))
