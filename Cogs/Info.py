from discord.ext import commands
import discord

from bot_data import embed_colors, help_embed


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help2')
    async def help2(self, ctx):
        embed = discord.Embed(title='Help')
        for category in help_embed:
            s = ''
            for cmd in help_embed[category]:
                cmd2 = help_embed[category][cmd]
                s += f'**{cmd}:** *{cmd2["syntax"]} {" = " + cmd2["info"] if cmd2["info"] else ""}*\n'
            embed.add_field(name=f'__{category}__', value=s, inline=False)

        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        await ctx.send(embed=embed)
   
    @commands.command(name='help', description='The help command!',
                      aliases=['commands', 'command'], usage='cog')
    async def help_command(self, ctx, cog='all'):
        """
        The third parameter comes into play when
        only one word argument has to be passed by the user
        """

        # Prepare the embed
        help_embed = discord.Embed(title='Help', color=embed_colors['info'])
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.bot.user.avatar_url)

        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]
        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            for cog in cogs:
                if cog == "Events": pass
                else:
                    # Get a list of all commands under each cog

                    cog_commands = self.bot.get_cog(cog).get_commands()
                    commands_list = ""
                    for comm in cog_commands:
                        commands_list += f'**{comm.name}** - *{comm.description}*\n'
                        # - *{comm.description}*
                    # Add the cog's details to the embed.

                    help_embed.add_field(name=cog, value=commands_list, inline=False)
                    # Also added a blank field '\u200b' is a whitespace character.
        else:
            # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:

                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[lower_cogs.index(cog.lower())]).get_commands()
                help_text = ''

                # Add details of each command to the help text
                # Command Name
                # Description
                # [Aliases]
                #
                # Format
                for command in commands_list:
                    help_text += f'```{command.name}```\n' \
                        f'**{command.description}**\n\n'

                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_text += f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n\n'
                    else:
                        # Add a newline character to keep it pretty
                        # That IS the whole purpose of custom help
                        help_text += '\n'

                    # Finally the format
                    help_text += f'Format: `@{self.bot.user.name}#{self.bot.user.discriminator}' \
                        f' {command.name} {command.usage if command.usage is not None else ""}`\n\n\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=help_embed)
    
        return

    @commands.command(pass_context=True, description="Manages polls")
    async def poll(self, ctx, cord: str, var, *options: str):
        """
        Creates a poll.
        :param ctx: channel where the command was used
        :param cord: whether to create or end poll
        :param var: The (Ultimate) question (of Life, the Universe, and Everything)
        :param options: vote options
        :return: None
        """
        if cord.lower() == "create":
            if len(options) <= 1:
                await ctx.send('You need more than one option to make a poll!')
                return
            if len(options) > 10:
                await ctx.send('You cannot make a poll for more than 10 things!')
                return
            if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
                reactions = ['✅', '❌']
            else:
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
            description = []
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title=var, description=''.join(description), color=0x0000FF)
            react_message = await ctx.send(embed=embed)
            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)
            embed.set_footer(text='Poll ID: {}'.format(react_message.id))

            await react_message.edit(embed=embed)
        elif cord.lower() == "end":
            poll_message = await ctx.channel.fetch_message(var)
            embed = poll_message.embeds[0]
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
                else {x[:1]: x[2:] for x in unformatted_options}

            # check if we're using numbers for the poll, or x/checkmark, parse accordingly
            voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes
            tally = {x: 0 for x in opt_dict.keys()}
            for reaction in poll_message.reactions:
                if reaction.emoji in opt_dict.keys():
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1
                            voters.append(reactor.id)
            output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(
                ['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
            await ctx.send(output)

        else:
            await ctx.send("Correct syntax: `!poll <create/end>`")

    @commands.command(pass_context=True, description="TOD0TODOTODOTODO")
    async def todo(self, ctx):
        todo_str = """.
        TODO:
        - settings?
        - maybe some moderation? (f-words etc.)
        - bind user to MC account
        - store all these things in JSON
        (maybe YAML if it could work? idk, didn't work with it)
        - mute command
        - test everything on you new friend
        """

        for i in todo_str.split('\n'):
            await ctx.send(i if i else '.')


def setup(bot):
    bot.add_cog(Info(bot))
