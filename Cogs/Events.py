import sys
import logging as log
import hashlib as h
import bot_data as bd

from discord.ext import commands
import discord


class Events(commands.Cog):  # TODO: Add proper documentation to the class + methods
    def __init__(self, bot):
        self.bot = bot
        self.safe_block = False

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="on developer's nerves"))
        # await self.bot.get_channel(781492333967179821).send('Bot successfully started')

        print('Bot successfully started')

    # ----- Handling errors -----
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Called when an error occurs during a processing of a command
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

        await ctx.send(embed=bd.error_embed(error_message,
                                            description='An error occurred while processing the command!')
                       )

    # ----- Giving out Guest role when user joins -----
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        When a member joins give him the "Guest" role
        and send him welcome message into DMs.
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
                                      description=f"Welcome {member.mention} to the official\nWynnic Rebellion discord server!",
                                      color=bd.embed_colors['normal'])
        welcome_embed.add_field(name='How to get started:', value='* Read the rules\n* Get a guild role')
        welcome_embed.add_field(name='What *not* to do', value='* Break the rules')
        welcome_embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        await member.send(embed=welcome_embed)

    # ----- Making commands case insensitive -----
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        What to do when any message is sent.
        :param message: message sent
        :return: None
        """

        if self.safe_block and message.content[0] == '!':
            await self.bot.get_user(552883527147061249).send('Failsafe activated')
            print('Failsafe activated.')
            log.warning('Failsafe activated.')
            log.shutdown()
            sys.exit('Command sent')
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        for role in message.author.roles:
            if role.name == 'muted':
                await message.delete()

        temp = message.content.split(" ")
        message.content = str(temp[0].lower())
        for x in temp[1:]:
            message.content += " " + str(x)
            
        if message.content == "cktq:4":
            await message.channel.send("ahoj")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # TODO: either remove or do something with it
        # channel = await self.bot.fetch_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)
        # user = await self.bot.fetch_user(payload.user_id)
        # emoji = payload.emoji.name
        pass

    @commands.command()
    async def failsafe(self, ctx, code: str):
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

        await ctx.message.delete()
        await ctx.send('Successfully blocked')
        await ctx.author.send('Failsafe activated primed')
        print('Failsafe activated primed')
        log.warning('Failsafe activated primed')
        self.safe_block = True


def setup(bot):  # TODO: what documentation to add here?
    bot.add_cog(Events(bot))
