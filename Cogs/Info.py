"""
Module for class containing informational commands
"""
__all__ = [
    'Events',
    'setup'
]

import discord
from discord.ext import commands

import bot_data as bd
import util


class Info(commands.Cog):
    """
    This class handles informational commands
    """
    description_ = 'Informational commands'

    def __init__(self, bot: util.CustomBot):
        self.bot = bot

    @commands.command(usage='ping',
                      description='Command for getting bot latency')
    async def ping(self, ctx: commands.Context):
        """
        Command for checking latency

        :param ctx: context of the message
        """
        await ctx.send(f'Bot\' latency is {self.bot.latency*1000:.3f}ms')

    @commands.command(aliases=['info', 'information'], usage='help [page]',
                      description='Command for displaying help embed')
    async def help(self, ctx: commands.Context, page: int = 1):
        """
        Command for displaying help embeds. Pages can be changed via reactions (implemented in on_raw_reaction_add)

        :param ctx: context of the message
        :param page: page to display; defaults to 1
        """

        all_cogs = util.get_cog_name_list(self.bot)  # get list of all cogs except Events
        if not (1 <= page <= len(all_cogs)+1):  # if it is not a valid page send an error; +1 for general help
            await ctx.send(embed=util.error_embed(f'The page must be between 1 and {len(all_cogs)}'))
            return

        message = await ctx.send(embed=_help_embed(self.bot, page-1))  # send the message

        # add reactions
        await message.add_reaction('◀')  # back
        await message.add_reaction('1️⃣')  # to the first page
        await message.add_reaction('⏹')  # block page moving
        await message.add_reaction('▶')  # forward

    # TODO: Options
    #   1) make listener for each thing
    #   2) make it all one big function
    #   3) make 1 listener that calls other functions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Listener for adding reactions

        DETAIL: if the reaction is the first one of its type used,
            it seems to have an extra space ('▶ ' instead of '▶')

        :param payload:  information regarding the emoji
        """
        if self.bot.get_user(payload.user_id).bot:  # if the user is a bot ignore it
            return

        emoji = str(payload.emoji.name)  # get the emoji
        channel = self.bot.get_channel(payload.channel_id)  # get the channel
        message = await channel.fetch_message(payload.message_id)  # get the message

        # ---------- help embed ----------
        # if it has an embed; if the embed is the help one; if the reaction is a forward or back arrow
        if message.embeds and 'Help page' in message.embeds[0].title and emoji in ('▶', '◀', '⏹', '1️⃣'):
            all_cogs = util.get_cog_name_list(self.bot)
            message_index = int(message.embeds[0].title.split('\n')[0][-1])  # number in the title

            if emoji == '▶':  # go forward
                index = message_index  # which cog to choose ( no change because of indexing
                if index >= len(all_cogs)+1:  # if it is the last page -> go to the first one; +1 for general help
                    index = 0
            elif emoji == '◀':  # go backwards
                index = message_index - 2  # which cog to choose (-2 for indexing)
                if index <= -1:  # if it is the first page -> go to the last one
                    index = len(all_cogs)

            elif emoji == '⏹':  # prevent the embed from changing TODO: test with multiple users
                await message.clear_reactions()
                return

            elif emoji == '1️⃣':  # go to the fi
                index = 0

            else:
                return  # to make IDE happy

            await message.remove_reaction(emoji, payload.member)  # remove the reaction (so the user doesn't have to do it)
            await message.edit(embed=_help_embed(self.bot, index))  # edit the embed


def _help_embed(bot: util.CustomBot, index: int) -> discord.Embed:
    """
    Helper function for creating a help embed
    :param bot: the bot instance
    :param index: what page to create
    :return: help embed
    """
    if index == 0:  # first page -> general information
        embed = discord.Embed(
            title=f'Help page {index + 1}\nGeneral information',
            description=f'Some bot\'s description I can\'t think of now'
                        f'\n\nBot\'s prefix: \'{bot.config["prefix"]}\''
                        f'\n\nAuthors:'
                        '\n- Astolfo_for_life (original bot)'
                        '\n- TrapinchO (original and new bot)',
            colour=bd.embed_colors['info'],
        )
        embed.set_thumbnail(url=bot.config['embed_image_url'])
        return embed

    all_cogs = util.get_cog_name_list(bot)
    cog_name = all_cogs[index-1]  # get the cog's name

    embed = discord.Embed(  # change the embed
        title=f'Help page {index + 1}\nCategory: {cog_name}',
        description=_help_cog(bot.get_cog(cog_name)),  # get the cog help
        colour=bd.embed_colors['info']
    )
    embed.set_thumbnail(url=bot.config['embed_image_url'])
    return embed


def _help_cog(cog: commands.Cog) -> str:
    """
    Helper function for generating command list string

    :param cog: cog to get help for
    :return: help string
    """
    # the underscore is there to differentiate from default attribute
    # default is class' docstring
    commands_list = '\n' + (cog.description_ if hasattr(cog, 'description_') else '') + '\n\n'

    for command in cog.get_commands():
        # Add the cog's details to the embed.
        commands_list += f'**{command.name}**:' \
                         f'\n- Usage: *{command.usage}*' \
                         f'\n- Description: *{command.description}*' + \
                         (f'\n- Aliases: *{" ".join(command.aliases)}*' if command.aliases else '') + \
                         '\n'
    # if there are no non-whitespace character (not description or commands) send "nothing"
    # in theory shouldn't happen outside dev environment
    return commands_list if commands_list.strip() else 'nothing'


def setup(bot: util.CustomBot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Info(bot))
