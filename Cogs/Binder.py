from typing import Union

from discord.ext import commands
import discord

from Wrappers.player import Player


class Binder(commands.Cog):  # TODO: finish it
    player_list = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bind(self, ctx, username: Union[discord.Member, str], highest_lvl: str):
        player_name = Player(username)
        if not player_name.found:
            await ctx.channel.send(f'Player name \"{username}\" was not found')

        elif player_name['highest level combat'] == highest_lvl:
            Binder.player_list[ctx.author.id] = username
            await ctx.channel.send(player_name['highest level combat'])
            await ctx.channel.send(Binder.player_list)
        else:
            await ctx.channel.send('Incorrect highest level')


def setup(bot):
    bot.add_cog(Binder(bot))
