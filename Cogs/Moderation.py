from discord.ext import commands
import discord
import logging as l
import bot_data as bd


class Moderation(commands.Cog):
    """
    This class handles moderation commands
    Current features:
    - mute <member> [reason]
    !!!- unmute = not implemented
    - kick <member> [reason]
    - ban <member> [reason]
    - say = make the bot repeat

    FOR TESTING PURPOSES permissions are not required
    """
    def __init__(self, bot):
        self.bot = bot

    # ----- mute -----
    @commands.command(description="mutes the user", usage="!mute <user> [reason]")
    # @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, user: discord.Member, *, reason: str = 'No reason provided'):
        """
        Used to mute players.
        Requires "kick" permission.

        :param ctx: channel where the command was used
        :param user: who was muted
        :param reason: reason for the mute
        :return: None
        """
        # TODO: Make it work properly even when the bot if offline (aka remove their perms to send messages)
        l.info(f'Muted user {user.name}. Reason: {reason}')

        try:
            await ctx.message.delete()
            await user.add_roles(discord.utils.get(user.guild.roles, name='muted'))
            await self.bot.get_channel(782625707963842600).send(embed=log_embed('Mute', ctx.author, user, reason))
            await ctx.channel.send(embed=action_embed('Muted', ctx, user, reason))
        except Exception as e:  # TODO: get what exception is raised
            await ctx.channel.send('Cannot assign role. Error: ' + str(type(e)))

    # ----- unmute -----
    @commands.command(description="unmutes the user", usage="!unmute <user>")
    # @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx: commands.Context, user: discord.Member):  # TODO: Implement it
        """
        Command to unmute user
        Not implemented

        :param ctx: channel where the command was used
        :param user: who was muted
        :return: None
        """
        l.info(f'Unmuted user {user.name}.')
        try:
            await ctx.message.delete()
            await user.remove_roles(discord.utils.get(user.guild.roles, name='muted'))
        except Exception as e:  # TODO: get what exception is raised
            await ctx.channel.send('Cannot unmute them. Error:\n' + str(type(e)))

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
        l.info(f'Kicked user {user.name}. Reason: {reason}')  # log it

        await user.kick(reason=reason)  # kick them

        kick_embed = action_embed('Kicked', ctx, user, reason)
        await ctx.message.delete()  # delete the message
        await ctx.channel.send(embed=kick_embed)  # send the message

        kick_embed.title = 'You were kicked!'
        await user.send(
            'Seems like you were not behaving properly.\nNext time please do not break the rules.',
            embed=kick_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Kick', ctx.author, user, reason)
        )

    #  ----- ban -----
    @commands.command(description="bans the user", usage="!ban <user> [reason]")
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason="No reason provided"):
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
        await user.send(
            'You broke the rules. A LOT.\nNow you have to face the consequences.\nWas it worth it?',
            embed=ban_embed)  # send it to the user's DMs

        await self.bot.get_channel(782625707963842600).send(
            embed=log_embed('Ban', ctx.author, user, reason)
            )

    @staticmethod
    async def censor(bot: discord.ext.commands.Bot, message: discord.Message):
        """
        Not a command. Used for moderating insults

        :param bot: Bot instance
        :param message: Message sent (to be processed)
        :return: None
        """
        mod_embed = discord.Embed(title='Inappropriate word', color=bd.embed_colors['moderation'])
        mod_embed.add_field(name='Author:', value=message.author.mention)

        bad_word_list = []
        text = ''
        lari_word = False  # TODO: I might be overdoing it
        for category in bd.bad_words:
            for word in bd.bad_words[category]:
                if word in message.content.lower():
                    bad_word_list.append(f'\"{word}\"')

                    if word == 'lari smart':  # mostly fun (unless...?)
                        await message.channel.send('*cough cough cough*')
                        lari_word = True
                    elif category == 'minor':  # minor insults that do not require much attention
                        lari_word = False
                    elif category == 'mid':  # quite offensive words
                        lari_word = False
                        await message.delete()
                    elif category == 'major':  # words requiring immediate moderator attention
                        lari_word = False
                        await message.delete()
                        text += '@Moderator'  # TODO: Mention all moderators

        if lari_word:
            return

        chat_embed = discord.Embed(color=bd.embed_colors['moderation'])
        chat_embed.add_field(name='User:', value=message.author.mention)
        chat_embed.add_field(name='Note:', value='Please refrain from using offensive words on this server.')
        await message.channel.send(embed=chat_embed)

        mod_embed.add_field(name='Word(s):', value=', '.join(bad_word_list))
        mod_embed.add_field(name='Message:', value=message.content)
        await bot.get_channel(782625707963842600).send(text, embed=mod_embed)

    # ----- repeat -----
    @commands.command(description="speak beep boop", usage="!say [args]")
    async def say(self, ctx: commands.Context, *, arg="Nothing"):
        """
        Friendly pudding's favourite command. Cannot be removed nor changed
        :param ctx: channel where the command was used
        :param arg: Message to say
        :return: None
        """
        try: 
            await ctx.channel.send(str(arg))
        except Exception as e:
            await ctx.channel.send('Cannot assign role. Error: ' + str(e))


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
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
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
                          color=bd.embed_colors['moderation'])  # create embed
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png'
    )

    return embed


def setup(bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Moderation(bot))
