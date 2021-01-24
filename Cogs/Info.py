import asyncio as aio

import bot_data as bd

from discord.ext import commands
import discord


class Info(commands.Cog):
    """
    This class handles informational commands
    Current commands:
    - help
    - poll
    - too
    """

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, description="creates/ends poll",
                      usage="!poll <create|end> <name|message id> [options]")
    async def poll(self, ctx: commands.Context, cord: str, var, *options: str):  # TODO: add documentation, a lot of it
        """
        Manages a poll.
        - create
          - !poll create <question> <options separated by space>
        - end
          - !poll end <poll id>

        FriendlyPudding shall document it themselves

        :param ctx: channel where the command was used
        :param cord: whether to create or end poll
        :param var: The (Ultimate) question (of Life, the Universe, and Everything)
        :param options: vote options
        :return: None
        """
        if cord.lower() == "create":  # creating a poll
            if len(options) < 2:  # not enough options
                await ctx.send('You need more than one option to make a poll!')
                return
            if len(options) > 10:  # too many options
                await ctx.send('You cannot make a poll for more than 10 things!')
                return
            if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
                reactions = ['✅', '❌']  # yes/no poll get special reactions
            else:  # proper poll
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']  # TODO: Maybe use unicode code?
                # reactions = [
                #     '\U000020E3', '\U000020E3', '\U000020E3', '\U000020E3', '\U000020E3',
                #     '\U000020E3', '\U000020E3', '\U000020E3', '\U000020E3', '\U0001F51F'
                # ]  # This one apparently doesn't work (I wonder why...)

            description = []  # create embed text
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)

            embed = discord.Embed(title=var, description=''.join(description), color=0x0000FF)
            react_message = await ctx.send(embed=embed)

            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)

            embed.set_footer(text='Poll ID: {}'.format(react_message.id))

            await react_message.edit(embed=embed)

        elif cord.lower() == "end":  # ending a poll
            # TODO: FriendlyPudding please clear this mess, or at least comment it
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
                [f'{opt_dict[key]}: {tally[key]}' for key in tally.keys()])
            await ctx.send(output)
            # TODO: End of mess

        else:
            await ctx.send("Correct syntax: `!poll <create/end>`")

    @commands.command(description="TOD0 list", usage="!todo")
    async def todo(self, ctx):
        embed = discord.Embed(title='TODO:', color=bd.embed_colors['info'])
        embed.add_field(name='todo', value=bd.todo_str)

        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['commands', 'command'],
                      usage="!help [cog]", description="displays this message")
    async def help(self, ctx, cog='all'):
        embed = discord.Embed(
            title='Help', color=bd.embed_colors['info'])
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png')
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url)

        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]
        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            for cog in cogs:
                if cog != "Events":
                    # Get a list of all commands under each cog

                    cog_commands = self.bot.get_cog(cog).get_commands()
                    commands_list = ""
                    for comm in cog_commands:
                        commands_list += f'**{comm.name}**: *{comm.usage}* *=* *{comm.description}*\n'
                    # Add the cog's details to the embed.
                    embed.add_field(name=f'__{cog}__', value=commands_list, inline=False)

        else:
            if cog.lower() in ('events', 'bunny'):
                await ctx.channel.send('Module not found')
                return
            # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:
                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[lower_cogs.index(cog.lower())]).get_commands()
                help_text = f'__{cog}:__\n' + '\\_'*32 + '\n'

                for command in commands_list:
                    help_text += f'__{command.name}__\n'
                    help_text += f'Description: {command.description}\n'

                    if len(command.aliases) > 0:  # Also add aliases, if there are any
                        help_text += f'Aliases: `{"`, `".join(command.aliases)}`\n'

                    # Finally the format
                    help_text += f'Usage: `{command.usage if command.usage is not None else ""}`\n'

                embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=embed)
    
        return

    @commands.command(usage='!timer <amount> <unit>', description='Sets timer to <amount> <unit>')
    async def timer(self, ctx: commands.Context, time: str, units: str):
        """
        Simple timer

        :param ctx: channel where the command was used
        :param time: time in units
        :param units: units of time used
        """
        time_units = {
            'second': ['second', 'seconds', 'sec', 's'],
            'minute': ['minute', 'minutes', 'min', 'm'],
            'hour': ['hour', 'hour', 'hr', 'h']
        }

        try:
            seconds = int(time)
        except ValueError:
            await ctx.channel.send(embed=bd.error_embed('Value error', 'Invalid number was passed'))
            return

        if units.lower() in time_units['second']:
            pass
        elif units.lower() in time_units['minute']:
            seconds *= 60
        elif units.lower() in time_units['hour']:
            seconds *= 3600
        else:
            await ctx.send(embed=bd.error_embed('Type error', 'Unknown unit of time'))
            return

        await ctx.send(f'Started timer for {time} {units}')
        await aio.sleep(seconds)
        await ctx.send(f'{ctx.author.mention} time is up!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Command for checking latency

        :param ctx: channel where the command was used
        :return: None
        """
        await ctx.send(f'Latency is {self.bot.latency*1000:.3f}ms')

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
            await ctx.send(str(arg))
        except Exception as e:
            await ctx.send('Cannot assign role. Error: ' + str(e))


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Info(bot))
