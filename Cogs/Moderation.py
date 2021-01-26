from discord.ext import commands
import discord
import logging
import bot_data as bd


class Moderation(commands.Cog):
    """
    This class handles moderation commands

    FOR TESTING PURPOSES permissions are not required
    """
    def __init__(self, bot):
        self.bot = bot

    # ----- mute -----
    @commands.command(description="mutes the user", usage="!mute <user> [reason]")
    # @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, user: discord.Member, reason: str = 'No reason provided'):
        """
        Used to mute players.
        Requires "kick" permission.

        :param ctx: channel where the command was used
        :param user: who was muted
        :param reason: reason for the mute
        :return: None
        """
        # TODO: Make it work properly even when the bot if offline (aka remove their perms to send messages)

        # If user does not have "muted" role (isn't muted)
        if not discord.utils.get(user.guild.roles, name='muted') in user.roles:
            await user.add_roles(discord.utils.get(user.guild.roles, name='muted'))  # Add the role

            await ctx.message.delete()
            await ctx.send(embed=action_embed('Muted', ctx, user, reason))  # Send embed to the channel
            await discord.utils.get(ctx.guild.channels, name="moderation-log").send(  # send embed to "moderation-log" channel
                embed=log_embed('Mute', ctx.author, user, reason)
            )
            log_text = f'Muted user {user.name}. Reason: {reason}'
            logging.info(log_text)
            print(log_text)

        else:  # Otherwise send error
            await ctx.send(embed=bd.error_embed('Human error', 'User is already muted'))

    # ----- unmute -----
    @commands.command(description="unmutes the user", usage="!unmute <user>")
    # @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx: commands.Context, user: discord.Member, reason=''):
        """
        Command to unmute user
        Not implemented

        :param reason: reason for unmute
        :param ctx: channel where the command was used
        :param user: who was muted
        :return: None
        """

        # If user does has "muted" role (is muted)
        if discord.utils.get(user.guild.roles, name='muted') in user.roles:
            await user.remove_roles(discord.utils.get(user.guild.roles, name='muted'))  # Remove the role

            await ctx.message.delete()
            await ctx.send(embed=action_embed('Unmuted', ctx, user, 'reason'))  # send embed into the channel
            await discord.utils.get(ctx.guild.channels, name="moderation-log").send(  # send embed into "moderation-log" channel
                embed=log_embed('Unmute', ctx.author, user, reason)
            )
            log_text = f'Unmuted user {user.name}. Reason: {reason}'
            logging.info(log_text)
            print(log_text)

        else:  # Otherwise send error
            await ctx.send(embed=bd.error_embed('Human error', 'User is not muted'))

    # ----- kick -----
    @commands.command(description="kicks the user", usage="!kick <user> [reason]")
    # @commands.has_permissions(kick_members=True)
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
        await user.send(
            'Seems like you were not behaving properly.\nNext time please do not break the rules.',
            embed=kick_embed)  # send it to the user's DMs

        await discord.utils.get(ctx.guild.channels, name="moderation-log")(
            embed=log_embed('Kick', ctx.author, user, reason)
        )

    #  ----- ban -----
    @commands.command(description="bans the user", usage="!ban <user> [reason]")
    # @commands.has_permissions(ban_members=True)
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
        await user.send(
            'You broke the rules. A LOT.\nNow you have to face the consequences.\nWas it worth it?',
            embed=ban_embed)  # send it to the user's DMs

        await discord.utils.get(ctx.guild.channels, name="moderation-log").send(
            embed=log_embed('Ban', ctx.author, user, reason)
            )

    @commands.command()
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

        embed = discord.Embed(  # creating the embed
            title='Member report',
            color=bd.embed_colors['moderation']
        )
        embed.add_field(name='Reported user:', value=member.mention)
        embed.add_field(name='By:', value=ctx.author.mention)
        embed.add_field(name='Reason:', value=' '.join(reason), inline=False)

        await ctx.send('Warning:\n**Misuse of this command will be punished**', embed=embed)
        await discord.utils.get(ctx.guild.channels, name="moderation-log").send(embed=embed)

    @staticmethod
    async def censor(message: discord.Message):
        """
        Not a command. Used for moderating insults

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
                        text = '@Moderator'  # TODO: Mention all moderators

        chat_embed = discord.Embed(color=bd.embed_colors['moderation'])
        chat_embed.add_field(name='User:', value=message.author.mention)
        chat_embed.add_field(name='Note:', value='Please refrain from using offensive words on this server.')
        await message.channel.send(embed=chat_embed)

        mod_embed = discord.Embed(title='Inappropriate word', color=bd.embed_colors['moderation'])  # TODO: fix
        mod_embed.add_field(name='Author:', value=message.author.mention)
        mod_embed.add_field(name='Word(s):', value=', '.join(bad_word_list))
        mod_embed.add_field(name='Message:', value=message.content)

        await discord.utils.get(
            message.guild.text_channels, name="moderation-log"
        ).send(text, embed=mod_embed)


def log_embed(action: str, author: discord.Member, user: discord.Member, reason: str) -> discord.Embed:
    """
    Used to save some code

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
    embed.set_thumbnail(url=bd.embed_thumbnail)
    return embed


def action_embed(action: str, ctx: commands.Context, user: discord.Member, reason: str) -> discord.Embed:  # TODO: revisit
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
    embed.set_thumbnail(url=bd.embed_thumbnail)

    return embed


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Moderation(bot))
