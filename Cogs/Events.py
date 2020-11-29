from discord.ext import commands
import discord


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- Handling errors -----
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please pass in all requirements :rolling_eyes:.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have all the requirements :angry:")
        else:
            await ctx.send(error)

    # ----- Giving out Guest role when user joins -----
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.add_roles(discord.utils.get(member.guild.roles, name='guest'))
        except Exception as e:
            await print('Cannot assign role. Error: ' + str(e))
        welcome_embed = discord.Embed(title="Welcome!",
                                      description=f"Welcome {member.mention} to the official\nWynnic Rebellion discord server!",
                                      color=32768)
        welcome_embed.add_field(name='What to do', value='* Read the rules\n* Get a guild role')
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
            await message.channel.send("cktq:4")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name


def setup(bot):
    bot.add_cog(Events(bot))
