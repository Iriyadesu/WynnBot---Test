import re
import random as rnd

from discord.ext import commands
import discord

import bot_data as bd


class Miscellaneous(commands.Cog):
    @commands.command()
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


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Miscellaneous(bot))