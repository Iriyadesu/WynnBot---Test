"""
Module containing class for technical/debugging commands
"""
__all__ = [
    'Technical',
    'setup'
]

import json
import logging

import discord
from discord.ext import commands

import bot_data as bd
import util


# TODO: change as appropriate
def check_if_bot_dev(ctx: commands.Context):
    """
    Function for commands.check
    :param ctx: context of the message
    :return: if the message author is TrapinchO
    """
    #return ctx.author.id == <dev_ID>
    return True


class Technical(commands.Cog):
    """
    Class for technical commands.
    Made for the bot developers for debugging and stuff (especially when I can't get to the bot's host all the time
    """
    description_ = 'Technical commands\n**Do NOT use unless you are 101% sure!**'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='log <retrieve|level> [level]',
                      description='Commands for bot logging')
    @commands.has_permissions(administrator=True)
    @commands.check(check_if_bot_dev)
    async def log(self, ctx: commands.Context, action: str, level: str = None):
        """
        Command for working with bot logging
        :param ctx: context of the message
        :param action: action to take
        :param level: logging level to be set
        :return: None
        """
        if action.lower() == 'retrieve':
            with open('bot.log', 'rb') as file:
                await ctx.send(file=discord.File(file, 'bot.log'))

        elif action.lower() == 'level':
            if not level.upper() in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):  # if invalid level
                await ctx.send(embed=util.error_embed('Invalid logging level'))
                return

            logging.getLogger().setLevel(level.upper())  # change logging level
            await ctx.send(embed=discord.Embed(title=f"Logging",
                                               description=f"Successfully set logging level to {level.upper()}",
                                               color=bd.embed_colors['info']
                                               ))
        else:
            raise util.UnknownArgumentException('Unknown parameter passed')

    @commands.command(usage='config <retrieve|set>',
                      description='Commands for bot logging')
    @commands.has_permissions(administrator=True)
    @commands.check(check_if_bot_dev)
    async def config(self, ctx: commands.Context, action: str):
        """
        Command for working with bot config
        :param ctx: context of the message
        :param action: action to take
        :return: None
        """
        if action.lower() == 'retrieve':
            with open('config.json', 'rb') as file:
                await ctx.send(file=discord.File(file, 'config.json'))

        elif action.lower() == 'set':
            file = await util.file_attachment_to_str(ctx.message.attachments[0])  # get the file's content
            try:
                json.loads(file)
            except json.JSONDecodeError:  # if it is not JSON
                # TODO: OPTIONAL logging
                await ctx.send(embed=util.error_embed('Type error', 'Could not convert file to config file'))
                return

            util.set_config(self.bot, json.loads(file))

        else:
            raise util.UnknownArgumentException('Unknown parameter passed')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Technical(bot))
