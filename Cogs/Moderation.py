from discord.ext import commands
import discord
import logging as l

from bot_data import embed_colors


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- mute -----
    @commands.command(description="kicks someone")
    #@commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, *, reason='No reason provided'):
        """
        Used to mute players.
        Requires "kick" permission.
        :param ctx: channel where the command was used
        :param user: who was muted
        :param reason: reason for the mute
        :return: None
        """
        l.info(f'Muted user {user.name}. Reason: {reason}')

        try:
            await ctx.message.delete()
            await user.add_roles(discord.utils.get(user.guild.roles, name='muted'))
            await self.bot.get_channel(782625707963842600).send(
                embed=log_embed('Mute', ctx.author, user, reason))
        except Exception as e:
            await print('Cannot assign role. Error: ' + str(e))

    # ----- unmute -----
    @commands.command(description='unmute')
    async def unmute(self, ctx, user: discord.Member):
        l.info(f'Unmuted user {user.name}.')
        try:
            await ctx.message.delete()
            await user.remove_roles(discord.utils.get(user.guild.roles, name='muted'))
        except Exception as e:
            await print('Cannot unmute them. Error:\n' + str(e))

    # ----- kick -----
    @commands.command(description="kicks someone")
    #@commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        """
        Used to kick players.
        Requires "kick" permission.
        :param ctx: channel where the command was used
        :param user: who was kicked
        :param reason: reason for the kick
        :return: None
        """
        l.info(f'Kicked user {user.name}. Reason: {reason}')  # log it

        await user.kick(reason=reason)  # kick them

        kick_embed = action_embed('Kicked', ctx, user, reason)
        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=kick_embed)  # send the message

        kick_embed.title = 'You were kicked!'
        await user.send('Seems like you were not behaving properly.\nNext please do not break the rules.',
                        embed=kick_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Kick', ctx.author, user, reason)
        )

    #  ----- ban -----
    @commands.command(description="Bans someone")
    #@commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        """
        Used to ban players.
        Requires "ban" permission.
        :param ctx: channel where the command was used
        :param user: who was banned
        :param reason: reason for the ban
        :return: None
        """
        l.info(f'Banned user {user.name}. Reason: {reason}')  # log it

        await user.ban(reason=reason)  # ban them

        ban_embed = action_embed('Banned', ctx, user, reason)
        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=ban_embed)  # send the message

        ban_embed.title = 'You were banned!'
        await user.send('You broke the rules. A LOT.\nNow you have to face the consequences.\nWas it worth it?',
                        embed=ban_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Ban', ctx.author, user, reason)
        )

    # ----- repeat -----
    @commands.command(description="speak beep boop")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg="Nothing"):
        try: 
            await ctx.channel.send(str(arg))
        except Exception as e:
            await ctx.channel.send('Cannot assign role. Error: ' + str(e))


def log_embed(action, author: discord.Member, user: discord.Member, reason: str):
    """
    Used to save some code
    :param action: action taken; currently ['ban', 'kick', 'mute']
    :param author: who used that command
    :param user: again who was the action taken (e.g. who was banned)
    :param reason: reson for the action
    :return: discord.Embed
    """
    embed = discord.Embed(title=action, color=embed_colors['moderation'])
    embed.add_field(name='By:', value=author.mention)
    embed.add_field(name='Who:', value=user.mention)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name='Reason:', value=reason)
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
    return embed


def action_embed(action: str, ctx, user: discord.Member, reason: str):
    """
    Function for generating moderator embeds
    :param action: action taken
    :param ctx: channel where the command was used
    :param user: again who was the action taken (e.g. who was banned)
    :param reason: reason for the action
    :return: discord.Embed
    """
    embed = discord.Embed(title=f":boom: {action} {user.name}!",
                          description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                          color=embed_colors['moderation'])  # create embed
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png'
    )

    return embed


def setup(bot):
    bot.add_cog(Moderation(bot))
