import sys
import logging as log
import hashlib as h
import bot_data as bd

from discord.ext import commands
import discord

from Cogs import Moderation


class Events(commands.Cog):
    """
    This class works with events (e.g. someone sends a message)
    Current events:
    - bot is done with initialisation
    - new member joins
    - message sent
    - reaction added
    """
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.safe_block = False

    @commands.Cog.listener()
    async def on_connect(self):
        """
        Called when bot is connected
        - log it
        """
        print('Bot connected')
        log.info('Bot connected')

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Called when the bot is ready
        - log it
        - change status
        """
        # TODO: Add init to things like channels (moderation-log), maybe roles (Moderator)?

        print('Bot ready')
        log.info('Bot ready')
        await self.bot.change_presence(activity=discord.Game(name="on developer's nerves"))
        # await self.bot.get_channel(781492333967179821).send('Bot successfully started')

    @commands.Cog.listener()
    async def on_disconnect(self):
        """
        Called when bot is disconnected
        - log it
        """
        print('Bot disconnected')
        log.info('Bot disconnected')

    # ----- Handling errors -----
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """
        Called when an error occurs during a processing of a command
        - get type of the error
        - send appropriate embed

        :param ctx: channel where the command was used
        :param error: type of error
        :return: none
        """
        if isinstance(error, commands.MissingRequiredArgument):
            error_message = 'Not enough arguments'
        elif isinstance(error, commands.MissingPermissions):
            error_message = 'Not enough permissions'
        else:
            error_message = str(error)

        await ctx.send(embed=bd.error_embed(str(error.__class__.__name__),
                                            error_message)
                       )

    # ----- Giving out Guest role when user joins -----
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Called when a member joins
        - give them role "Guest"
        - send them DM

        :param member: member that joined
        :return: None
        """
        log.info(f'New member joined! Username: {member.name}')
        try:
            await member.add_roles(discord.utils.get(member.guild.roles, name='guest'))
        except Exception as e:  # TODO: get type of raised exception
            print('Cannot assign role. Error: ' + str(e))
        # ----- create the embed -----
        welcome_embed = discord.Embed(title="Welcome!",
                                      description=f"Welcome {member.mention} to the official"
                                                  f"\nWynnic Rebellion discord server!",
                                      color=bd.embed_colors['normal'])
        welcome_embed.add_field(name='How to get started:', value='* Read the rules\n* Get a guild role')
        welcome_embed.add_field(name='What *not* to do', value='* Break the rules')
        welcome_embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        await member.send(embed=welcome_embed)

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
        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        elif any(word in message.content.lower() for word in bd.bad_words_list):
            await Moderation.Moderation.censor(message)
            return

        elif self.safe_block and message.content[0] == '!':
            await self.bot.get_user(552883527147061249).send('Failsafe activated')
            print('Failsafe activated.')
            log.error('Failsafe activated.')
            log.shutdown()  # so there is no error sent
            sys.exit('Command sent')

        # TODO: Create a proper mute

        temp = message.content.split(" ")
        message.content = str(temp[0].lower())
        for x in temp[1:]:
            message.content += " " + str(x)
            
        if message.content == "cktq:4":
            await message.channel.send("ahoj")

    @commands.command()
    async def failsafe(self, ctx, code: str):
        """
        A command
        """
        await ctx.message.delete()

        if ctx.author.id != 552883527147061249 and ctx.author.id != 345167339693670430:
            await ctx.send('Inappropriate user')
            return

        try:
            with open('../padej.txt', 'r') as f:
                failsafe_code = f.read()
        except FileNotFoundError:
            failsafe_code = 'kharaa'

        if h.new('sha256', code.encode()).hexdigest() != h.new('sha256', failsafe_code.encode()).hexdigest():
            await ctx.send('Wrong password')
            return

        await ctx.send('Successfully blocked')
        await ctx.author.send('Access granted. Proceed with caution')
        print('Failsafe primed')
        log.warning('Failsafe primed')
        self.safe_block = True

    @commands.command()
    async def lari_smart(self, ctx: commands.Context):
        await ctx.channel.send('*cough*')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Events(bot))
