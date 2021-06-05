"""
Module for class containing events functions
"""
__all__ = [
    'Events',
    'setup',
]

import hashlib as h
import logging

import discord
from discord.ext import commands

import bot_data as bd
import util
from Cogs import Moderation


class Events(commands.Cog):
    """
    This class works with events (e.g. someone sends a message)
    """
    description_ = 'Internal events'

    def __init__(self, bot: util.CustomBot):
        self.bot = bot
        self.safe_block = False

    @commands.Cog.listener()
    async def on_connect(self):
        """
        Called when bot is connected
        - log it
        """
        util.log_print('Bot connected')

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Called when the bot is ready
        - log it
        - change status
        """
        util.log_print('Bot ready')

        await self.bot.change_presence(activity=discord.Game(name="on developer's nerves"))

    @commands.Cog.listener()
    async def on_disconnect(self):
        """
        Called when bot is disconnected
        - log it
        """
        util.log_print('Bot disconnected')

    @commands.Cog.listener()
    async def on_resumed(self):
        """
        Called when bot has resumed connection
        """
        util.log_print('Bot has resumed connection')

    # ----- Giving out Guest role when user joins -----
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Called when a member joins
        - give them role "Guest"
        - send them DM

        :param member: member that joined
        """
        # logging.info(f'New member joined! Username: {member.name}')
        # await member.add_roles(discord.utils.get(member.guild.roles, name='guest'))
        # ----- create the embed -----
        welcome_embed = discord.Embed(title="Welcome!",
                                      description=f"Welcome {member.mention} to our server",
                                      color=bd.embed_colors['normal'])
        welcome_embed.add_field(name='How to get started:', value='* Read the rules')
        welcome_embed.add_field(name='What *not* to do', value='* Break the rules')
        welcome_embed.set_thumbnail(url=self.bot.config['embed_image_url'])
        await member.send(embed=welcome_embed)

    # ----- Handling errors -----
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """
        Called when an error occurs during a processing of a command
        - get type of the error
        - send appropriate embed

        :param ctx: channel where the command was used
        :param error: type of error
        :return: None
        """
        # TODO: Other's permission!
        print(f'{"-"*32}'
              f'\n!!! Error:'
              f'\n!!! {error.__class__.__name__}'
              f'\n!!! {error}'
              f'\n!!! Message: {ctx.message.content}'
              f'\n{"-"*32}'
              )
        logging.error(f'An error occurred during command handling: {error!r}')

        if isinstance(error, commands.MissingRequiredArgument):
            error_name = ('Not enough arguments were passed',
                          None)
        elif isinstance(error, commands.MissingPermissions):
            error_name = ('Not allowed to use the command',
                          None)
        elif isinstance(error, commands.CommandNotFound):  # if command was not found ignore it
            error_name = ('Command not found',
                          None)
        elif isinstance(error, commands.MemberNotFound):  # if there should've been mention or the name couldn't be converted to mention
            error_name = ('Member not found'
                          '\nPlease mention requested user', None)
        elif isinstance(error, util.UnknownArgumentException):
            error_name = ('Unknown argument',
                          None)
        elif isinstance(error, commands.BadArgument):
            error_name = ('Value error',
                          'Couldn\'t process value')
        else:  # something I have no idea of
            await ctx.send(
                embed=util.error_embed('Unexpected error',
                                       'An unexpected error occurred.'
                                       'Please contact thee bot\'s author to fix it for a fix.'))
            raise error

        await ctx.send(
            embed=util.error_embed(*error_name,
                                   usage=f'{self.bot.config["prefix"]}{ctx.command.signature}' if ctx.command else None)
        )

    # ----- Making commands case insensitive -----
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Called when a message was sent
        - prevent bot reacting to their own messages
        - prepare message for eventual command evaluation

        :param message: message sent
        :return: None
        """
        # TODO: Doesn't block entirely
        # The command is always carried out, no matter the result of this function
        if not isinstance(message.channel, discord.TextChannel):  # ignoring private channels for now
            return

        if message.author == self.bot.user:  # if it was sent by the bot itself
            return

        if message.author.bot:  # if it is bot account in general
            return

        # invoke "info" command by mentioning the bot
        if self.bot.user.mentioned_in(message):
            ctx = await self.bot.get_context(message)  # get context for later processing
            await ctx.invoke(self.bot.get_command('help'))  # invoke "help" command
            return

        if any(word in message.content.lower() for word in bd.bad_words_list) and message.content[0] != '!':
            # TODO: better fix
            #   Probably remove
            await Moderation.Moderation.censor(self.bot, message)
            return

        if self.safe_block and message.content[0] == '!':
            await self.bot.get_user(552883527147061249).send('Failsafe activated')
            util.log_print('Failsafe activated', 'WARNING')

            logging.shutdown()  # so there is no error sent
            # TODO: attempt to disable block command execution
            # still executes the command (though it is really disabled)
            # self.bot.remove_command(message.content.split(" ")[0][1:].lower())
            await self.bot.close()
            return

        temp = message.content.split(" ")
        message.content = temp[0].lower() + ' ' + ' '.join(temp[1:])

    @commands.command()
    async def failsafe(self, ctx: commands.Context, code: str):  # TODO: Why not shut down the bot directly?
        """
        A command
        """
        await ctx.message.delete()

        if ctx.author.id != 552883527147061249:  # if it is not me (TrapinchO)
            await ctx.send('Inappropriate user')
            return

        try:
            with open('../failsafe.txt', 'r') as file:
                failsafe_code = file.read()
        except FileNotFoundError:
            failsafe_code = 'kharaa'

        if h.new('sha256', code.encode()).hexdigest() != h.new('sha256', failsafe_code.encode()).hexdigest():
            await ctx.send('Wrong password')
            return

        await ctx.send('Successfully blocked')
        await ctx.author.send('Access granted. Proceed with caution')
        util.log_print('Failsafe primed', 'WARNING')
        self.safe_block = True  # primes the failsafe


def setup(bot: util.CustomBot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Events(bot))
