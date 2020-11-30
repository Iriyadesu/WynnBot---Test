from discord.ext import commands
import discord
import logging as l


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #  ----- ban -----
    @commands.command(description="Bans someone")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        l.info(f'Banned user {user.name}. Reason: {reason}')  # log it

        await user.ban(reason=reason)  # ban them
        ban_embed = discord.Embed(title=f":boom: Banned {user.name}!",
                                  description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                  color=0xCCCC00)  # create embed

        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=ban_embed)  # send the message

        ban_embed.title = 'You were banned!'
        await user.send('You broke the rules. A LOT.\nNow you have to face the consequences.\nWas it worth it?',
                        embed=ban_embed)  # send it to the user's DMs

    # ----- kick -----
    @commands.command(description="kicks someone")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        l.info(f'Kicked user {user.name}. Reason: {reason}')  # log it

        await user.kick(reason=reason)  # kick them
        kick_embed = discord.Embed(title=f":boom: Kicked {user.name}!",
                                   description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                   color=0xCCCC00)  # create embed
        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=kick_embed)  # send the message

        kick_embed.title = 'You were kicked!'
        await user.send('Seems like you were not behaving properly.\nNext please do not break the rules.',
                        embed=kick_embed)  # send it to the user's DMs

    # ----- mute -----
    @commands.command(description="kicks someone")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.member, *, reason='No reason provided'):
        l.info(f'Muted user {user.name}. Reason: {reason}')

        pass

    # ----- repeat -----
    @commands.command(description="speak beep boop")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg="Nothing"):
        try: 
            await ctx.channel.send(str(arg))
        except Exception as e:
            await ctx.channel.send('Cannot assign role. Error: ' + str(e))


def setup(bot):
    bot.add_cog(Moderation(bot))
