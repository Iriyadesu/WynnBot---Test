from discord.ext import commands
import discord
import logging as l

from bot_data import embed_colors


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #  ----- ban -----
    @commands.command(description="Bans someone")
    #@commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        l.info(f'Banned user {user.name}. Reason: {reason}')  # log it

        await user.ban(reason=reason)  # ban them
        ban_embed = discord.Embed(title=f":boom: Banned {user.name}!",
                                  description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                  color=embed_colors['moderation'])  # create embed

        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=ban_embed)  # send the message

        ban_embed.title = 'You were banned!'
        await user.send('You broke the rules. A LOT.\nNow you have to face the consequences.\nWas it worth it?',
                        embed=ban_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Ban', ctx.author, user, reason)
        )

    # ----- kick -----
    @commands.command(description="kicks someone")
    #@commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        l.info(f'Kicked user {user.name}. Reason: {reason}')  # log it

        await user.kick(reason=reason)  # kick them
        kick_embed = discord.Embed(title=f":boom: Kicked {user.name}!",
                                   description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                   color=embed_colors['moderation'])  # create embed
        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=kick_embed)  # send the message

        kick_embed.title = 'You were kicked!'
        await user.send('Seems like you were not behaving properly.\nNext please do not break the rules.',
                        embed=kick_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Kick', ctx.author, user, reason)
        )

    # ----- mute -----
    @commands.command(description="kicks someone")
    #@commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, *, reason='No reason provided'):
        l.info(f'Muted user {user.name}. Reason: {reason}')

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Mute', ctx.author, user, reason)
        )

    # ----- repeat -----
    @commands.command(description="speak beep boop")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg="Nothing"):
        try: 
            await ctx.channel.send(str(arg))
        except Exception as e:
            await ctx.channel.send('Cannot assign role. Error: ' + str(e))


def log_embed(action, author, user, reason):
    log_embed = discord.Embed(title=action, color=embed_colors['moderation'])
    log_embed.add_field(name='By:', value=author.mention)
    log_embed.add_field(name='Who:', value=user.mention)
    log_embed.add_field(name=chr(173), value=chr(173))
    log_embed.add_field(name='Reason:', value=reason)
    return log_embed


def setup(bot):
    bot.add_cog(Moderation(bot))
