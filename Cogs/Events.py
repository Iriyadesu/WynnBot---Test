from discord.ext import commands
import discord
import logging as l

from bot_data import error_embed, embed_colors


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        await ctx.send(embed=error_embed(error_message,
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
        l.info(f'New member joined! Username: {member.name}')
        try:
            await member.add_roles(discord.utils.get(member.guild.roles, name='guest'))
        except Exception as e:
            await print('Cannot assign role. Error: ' + str(e))
        welcome_embed = discord.Embed(title="Welcome!",
                                      description=f"Welcome {member.mention} to the official\nWynnic Rebellion discord server!",
                                      color=embed_colors['normal'])
        welcome_embed.add_field(name='What to do', value='* Read the rules\n* Get a guild role')
        welcome_embed.add_field(name='What *not* to do', value='* Break the rules')
        welcome_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        await member.send(embed=welcome_embed)

    # ----- Making commands case insensitive -----
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        What to do when any message is sent.
        :param message: message sent
        :return: None
        """
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        temp = message.content.split(" ")
        message.content = str(temp[0].lower())
        for x in temp[1:]:
            message.content += " " + str(x)
            
        if message.content == "cktq:4":
            await message.channel.send("ahoj")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name


def setup(bot):
    bot.add_cog(Events(bot))
