from discord.ext import commands
import discord
import logging as l


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- Handling errors -----
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_ember = discord.Embed(title='Error',
                                    description='An error occurred while processing the command!',
                                    color=0)
        if isinstance(error, commands.MissingRequiredArgument):
            error_message = 'Not enough arguments'
        elif isinstance(error, commands.MissingPermissions):
            error_message = 'Not enough permissions'
        else:
            error_message = str(error)

        error_ember.add_field(name='Reason:', value=error_message)
        await ctx.send(embed=error_ember)

    # ----- Giving out Guest role when user joins -----
    @commands.Cog.listener()
    async def on_member_join(self, member):
        l.info(f'New member joined! Username: {member.name}')
        try:
            await member.add_roles(discord.utils.get(member.guild.roles, name='guest'))
        except Exception as e:
            await print('Cannot assign role. Error: ' + str(e))
        welcome_embed = discord.Embed(title="Welcome!",
                                      description=f"Welcome {member.mention} to the official\nWynnic Rebellion discord server!",
                                      color=32768)
        welcome_embed.add_field(name='What to do', value='* Read the rules\n* Get a guild role')
        welcome_embed.add_field(name='What *not* to do', value='* Break the rules')
        welcome_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        await member.send('Welcome!', embed=welcome_embed)

    # ----- Making commands case insensitive -----
    @commands.Cog.listener()
    async def on_message(self, message):
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
