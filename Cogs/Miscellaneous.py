import re
import random as rnd
import asyncio as aio

from discord.ext import commands
import discord

import bot_data as bd


class Miscellaneous(commands.Cog):

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
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣',
                             '🔟']  # TODO: Maybe use unicode code?
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

    @commands.command(
        description='Rolls dice for DnD',
        usage='!r <dice> [addition addition/subtraction]'
    )
    async def r(self, ctx: commands.Context, *args):
        """
        Command for rolling dice for DnD

        :param ctx: channel where the command was used
        :param args: roll message (in format {number of rolls}d{max roll} {optional: +/-number)
        :return:
        """
        # 1st group is number of rolls
        # 2nd group is the range <1; number> (inclusive)
        # 3rd group is addition number to add/subtract
        match = re.search(r'(\d+)d(\d+) *([+-] *\d+)?', ''.join(args))  # regex for getting the rolls
        if match is not None:  # if found
            roll_list = []
            for index in range(int(match.group(1))):
                roll_list.append(rnd.randint(1, int(match.group(2))))

            if match.group(3) is not None:  # TODO: fix "!r 1d20 +- 8" not raising an error
                last_part = f' {match.group(3)} = {sum(roll_list) + int(match.group(3))}'  # last part of the embed (the sum)
            else:
                last_part = f' +0 = {sum(roll_list)}'

            embed = discord.Embed(
                title=f'{match.group(1)}d{match.group(1)} rolls',
                color=bd.embed_colors['normal'],
                description=f'SUM: {sum(roll_list)}' + last_part
            )
            for index in range(len(roll_list)):  # display all rolls
                embed.add_field(name=f'Roll #{index + 1}', value=roll_list[index])

            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=bd.error_embed(
                'Human error', 'Invalid roll format'  # TODO: Make it better
            ))

    # ----- repeat -----
    @commands.command(description="speak beep boop", usage="!say [args]")
    async def say(self, ctx: commands.Context, *, arg="Nothing"):
        """
        Friendly pudding's favourite command. Cannot be removed nor changed
        :param ctx: channel where the command was used
        :param arg: Message to say
        :return: None
        """
        await ctx.send(str(arg))

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
            await ctx.send(embed=bd.error_embed('Value error', 'Invalid number was passed'))
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


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Miscellaneous(bot))
