"""
Module for class containing miscellaneous commands
"""
__all__ = [
    'Miscellaneous',
    'setup'
]

import asyncio as aio
import random as rnd
import re

import discord
from discord.ext import commands

import bot_data as bd
import util


class Miscellaneous(commands.Cog):
    """
    Class for miscellaneous commands
    """
    description_ = 'Miscellaneous commands'

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(usage="poll <create|result> <name|message id> [options]",
                      description="creates poll/send the result of a poll\npoll can have maximum of 10 options")
    async def poll(self, ctx: commands.Context, cord: str, var: str, *options: str):
        """
        Manages a poll.
        - create
          - !poll create <question> <options separated by space>
        - end
          - !poll result <poll id>

        :param ctx: channel where the command was used
        :param cord: whether to create or end poll
        :param var: The (Ultimate) question (of Life, the Universe, and Everything)
        :param options: vote options
        :return: None
        """
        # TODO: Possible multi-option poll?
        #   1) Separate action (by adding embed data?)
        #   2) Keep it as it is now (only one option per poll, first one counts)
        #   3) Make in multi-option by deleting the check
        if cord.lower() == "create":  # creating a poll
            if len(options) < 2:  # not enough options
                await ctx.send('You need more than one option to make a poll')
                return
            if len(options) > 10:  # too many options
                await ctx.send('You cannot make a poll for more than 10 options')
                return

            if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
                reactions = ['✅', '❌']  # yes/no poll get special reactions
            else:  # proper poll
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣',
                             '🔟']  # options 1-10

            description = ''  # create embed text
            for x, option in enumerate(options):
                description += f'\n {reactions[x]} {option}'

            embed = discord.Embed(title=var, description=description, color=0x0000FF)
            react_message = await ctx.send(embed=embed)  # send the message

            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)

            embed.set_footer(text='Poll ID: {}'.format(react_message.id))
            await react_message.edit(embed=embed)  # add message id to the poll (so it can be easily ended afterwards)

        elif cord.lower() == "result":  # ending a poll
            poll_message = await ctx.channel.fetch_message(var)
            embed = poll_message.embeds[0]
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            # check if we're using numbers for the poll, or x/checkmark, parse accordingly
            # key: emoji, value: option-text; example:  {'✅': 'yes', '❌': 'no'}
            if unformatted_options[0][0] == '1':
                option_dict = {x[:2]: x[3:] for x in unformatted_options}  # number poll
            else:
                option_dict = {x[:1]: x[2:] for x in unformatted_options}  # yes/no poll

            # check if we're using numbers for the poll, or x/checkmark, parse accordingly
            voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes
            tally = {x: 0 for x in option_dict.keys()}
            for reaction in poll_message.reactions:  # iterate through all
                if reaction.emoji not in option_dict:  # if it is not a valid option -> skip
                    continue
                async for reactor in reaction.users():  # iterate through the option
                    if reactor.id in voters:  # if the user hast already voted
                        continue
                    tally[reaction.emoji] += 1
                    voters.append(reactor.id)  # mark them as voted

            await poll_message.reply(embed=discord.Embed(  # reply to original poll message
                title=f'Results of the poll for:\n\'{embed.title}\'',
                description='\n'.join((f'- {option_dict[key]}: {tally[key]}' for key in tally.keys())),
                colour=bd.embed_colors['info']
            ))

        else:
            raise util.UnknownArgumentException('Unknown parameter passed')

    @commands.command(usage='r <dice> [addition addition/subtraction]',
                      description='Rolls dice for DnD')
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

        match = re.search(r'(\d+)d(\d+)([+-]\d+)?', ''.join(args))  # regex for getting the rolls
        if match is None or re.search(r'(\d+)d(\d+)((\+-)|(-\+)\d+)', ''.join(args)) is not None:  # if not found
            # '(\d+)d(\d+)((\+-)|(-\+)\d+)' --> "+-" should not work, so I check for it
            await ctx.send(embed=util.error_embed('Invalid roll format'))
            return

        roll_list = []
        for index in range(int(match.group(1))):
            roll_list.append(rnd.randint(1, int(match.group(2))))

        if match.group(3) is not None:
            last_part = f' {match.group(3)} = {sum(roll_list) + int(match.group(3))}'  # last part of the embed (the sum)
        else:
            last_part = f' +0 = {sum(roll_list)}'

        embed = discord.Embed(
            title=f'{match.group(1)}d{match.group(1)} rolls (by {ctx.author.name})',
            color=bd.embed_colors['normal'],
            description=f'SUM: {sum(roll_list)}' + last_part
        )
        for index in range(len(roll_list)):  # display all rolls
            embed.add_field(name=f'Roll #{index + 1}', value=roll_list[index])

        await ctx.send(embed=embed)

    @commands.command(usage='timer <amount> <unit>',
                      description='Sets timer to <amount> <unit>')
    async def timer(self, ctx: commands.Context, time: str, units: str):
        """
        Simple timer
        Multiple can be set at once, they use asyncio.sleep

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
            await ctx.send(embed=util.error_embed('Invalid number was passed'))
            return

        if units.lower() in time_units['second']:
            pass
        elif units.lower() in time_units['minute']:
            seconds *= 60
        elif units.lower() in time_units['hour']:
            seconds *= 3600
        else:
            await ctx.send(embed=util.error_embed('Unknown unit of time'))
            return

        await ctx.reply(f'Started timer for {time} {units}')
        await aio.sleep(seconds)  # wait until time is up
        await ctx.reply(f'Time is up!')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Miscellaneous(bot))
