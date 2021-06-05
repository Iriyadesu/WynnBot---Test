"""
Module containing class for moderation commands
"""
__all__ = [
    'Moderation',
    'setup'
]

import logging

import discord
from discord.ext import commands

import bot_data as bd
import util


class Moderation(commands.Cog):
    """
    This class handles moderation commands
    """
    description_ = 'Commands for moderation'

    def __init__(self, bot):
        self.bot = bot

    # ----- mute -----
    @commands.command(usage="mute <user> [reason]",
                      description="mutes the user")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, user: discord.Member, *, reason: str = 'No reason provided'):
        """
        Used to mute players.
        Requires "kick" permission.

        :param ctx: channel where the command was used
        :param user: who was muted
        :param reason: reason for the mute
        :return: None
        """
        # If user does already has "muted" role (is muted)
        if discord.utils.get(user.guild.roles, name=self.bot.config['mute_role']) in user.roles:
            await ctx.send(embed=util.error_embed('User is already muted'))
            return

        await user.add_roles(discord.utils.get(user.guild.roles, name=self.bot.config['mute_role']))  # Add the role

        await ctx.message.delete()
        await ctx.send(embed=action_embed('Muted', ctx, user, reason))  # Send embed to the channel
        await discord.utils.get(ctx.guild.channels, name=self.bot.config['moderation_log_channel']).send(
            embed=log_embed('Mute', ctx.author, user, reason, self.bot.config['embed_image_url'])  # send embed to "moderation-log" channel
        )
        util.log_print(f'Muted user {user.name}. Reason: {reason}')

    # ----- unmute -----
    @commands.command(usage="unmute <user>",
                      description="unmutes the user")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx: commands.Context, user: discord.Member, *, reason: str = 'No reason provided'):
        """
        Command to unmute user.
        Requires "kick" permission.

        :param reason: reason for unmute
        :param ctx: channel where the command was used
        :param user: who was muted
        :return: None
        """

        # If user does has "muted" role (is muted)
        if discord.utils.get(user.guild.roles, name=self.bot.config['mute_role']) not in user.roles:
            await ctx.send(embed=util.error_embed('User is not muted'))
            return

        await user.remove_roles(discord.utils.get(user.guild.roles, name=self.bot.config['mute_role']))  # Remove the role

        await ctx.message.delete()
        await ctx.send(embed=action_embed('Unmuted', ctx, user, reason))  # send embed into the channel
        await discord.utils.get(ctx.guild.channels, name=self.bot.config['moderation_log_channel']).send(
            embed=log_embed('Unmute', ctx.author, user, reason, self.bot.config['embed_image_url'])  # send embed into "moderation-log" channel
        )
        util.log_print(f'Unmuted user {user.name}. Reason: {reason}')

    # ----- kick -----
    @commands.command(usage="kick <user> [reason]",
                      description="kicks the user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason="No reason provided"):
        """
        Used to kick players.
        Requires "kick" permission.

        :param ctx: channel where the command was used
        :param user: who was kicked
        :param reason: reason for the kick
        :return: None
        """
        logging.info(f'Kicked user {user.name}. Reason: {reason}')  # log it

        await user.kick(reason=reason)  # kick them

        kick_embed = action_embed('Kicked', ctx, user, reason)
        await ctx.message.delete()  # delete the message
        await ctx.send(embed=kick_embed)  # send the message

        kick_embed.title = 'You were kicked!'
        await user.send(embed=kick_embed)  # send it to the user's DMs

        await discord.utils.get(ctx.guild.channels, name=self.bot.config['moderation_log_channel']).send(
            embed=log_embed('Kick', ctx.author, user, reason, self.bot.config['embed_image_url'])
        )

    #  ----- ban -----
    @commands.command(usage="ban <user> [reason]",
                      description="bans the user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason="No reason provided"):  # TODO: Check if embeds work
        """
        Used to ban players.
        Requires "ban" permission.

        :param ctx: channel where the command was used
        :param user: who was banned
        :param reason: reason for the ban
        :return: None
        """
        logging.info(f'Banned user {user.name}. Reason: {reason}')  # log it

        await user.ban(reason=reason)  # ban them

        ban_embed = action_embed('Banned', ctx, user, reason)
        await ctx.message.delete()  # delete the message
        await ctx.send(embed=ban_embed)  # send the message

        ban_embed.title = 'You were banned!'
        await user.send(embed=ban_embed)  # send it to the user's DMs

        await discord.utils.get(ctx.guild.channels, name=self.bot.config['moderation_log_channel']).send(
            embed=log_embed('Ban', ctx.author, user, reason, self.bot.config['embed_image_url'])
        )

    @commands.command(usage='report <member> [reason]',
                      description='Command for reporting members')
    async def report(self, ctx: commands.Context, member: discord.Member, *reason):
        """
        Command for reporting members

        The reason is used in this way so we can use more than 1 word

        :param ctx: context for the message
        :param member: reported member
        :param reason: reason for report
        :return: None
        """
        if not reason:  # if no reason was provided
            reason = 'No reason provided'
        else:
            reason = ' '.join(reason)

        embed = discord.Embed(  # creating the embed
            title='Member report',
            color=bd.embed_colors['moderation']
        )
        embed.add_field(name='Reported user:', value=member.mention)
        embed.add_field(name='By:', value=ctx.author.mention)
        embed.add_field(name='Reason:', value=reason, inline=False)

        await ctx.send('> Warning:\n> **Misuse of this command will be punished**', embed=embed)
        await discord.utils.get(ctx.guild.channels, name=self.bot.config['moderation_log_channel']).send(embed=embed)

    @commands.command(usage='purge <amount of messages to delete|10>',
                      description='Command for deleting messages in bulk')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context, limit: int = 10):
        """
        Command for deleting messages in bulk

        :param ctx: context of the message
        :param limit: amount of messages to be deleted
        :return: None
        """
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send(embed=discord.Embed(title='Success', description=f'Successfully purged {limit} messages'))

    @staticmethod
    async def censor(bot: util.CustomBot, message: discord.Message):
        """
        Not a command. Used for moderating insults

        :param bot: bot's instance; to retrieve the config
        :param message: Message sent (to be processed)
        :return: None
        """

        bad_word_list = []
        text = ''
        for category in bd.bad_words:
            for word in bd.bad_words[category]:
                if word in message.content.lower():
                    bad_word_list.append(f'\"{word}\"')

                    if category == 'minor':  # minor insults that do not require much attention
                        pass

                    elif category == 'mid':  # quite offensive words
                        await message.delete()

                    elif category == 'major':  # words requiring immediate moderator attention
                        await message.delete()
                        text = discord.utils.get(message.guild.roles, name=bot.config['moderator_role']).mention

        chat_embed = discord.Embed(color=bd.embed_colors['moderation'])
        chat_embed.add_field(name='User:', value=message.author.mention)
        chat_embed.add_field(name='Note:', value='Please refrain from using offensive words on this server.')
        await message.channel.send(embed=chat_embed)

        mod_embed = discord.Embed(title='Inappropriate word', color=bd.embed_colors['moderation'])
        mod_embed.add_field(name='Author:', value=message.author.mention)
        mod_embed.add_field(name='Word(s):', value=', '.join(bad_word_list))
        mod_embed.add_field(name='Message:', value=message.content)

        await message.channel.send(text, embed=mod_embed)


def log_embed(action: str, author: discord.Member, user: discord.Member, reason: str, thumbnail_url: str) -> discord.Embed:
    """
    Used to save some code

    :param thumbnail_url: thumbnail for the embed
    :param action: action taken; currently ['ban', 'kick', 'mute']
    :param author: who used that command
    :param user: again who was the action taken (e.g. who was banned)
    :param reason: reason for the action
    :return: discord.Embed
    """
    embed = discord.Embed(title=action, color=bd.embed_colors['moderation'])
    embed.add_field(name='By:', value=author.mention)
    embed.add_field(name='Who:', value=user.mention)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name='Reason:', value=reason)
    embed.set_thumbnail(url=thumbnail_url)  # TODO: possibly find a better solution; possibly through a function?
    return embed


def action_embed(action: str, ctx: commands.Context, user: discord.Member, reason: str) -> discord.Embed:
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
                          color=bd.embed_colors['moderation']
                          )  # create embed
    embed.set_thumbnail(url=ctx.bot.config['embed_image_url'])

    return embed


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Moderation(bot))
