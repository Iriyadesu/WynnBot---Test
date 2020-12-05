from typing import Union

from discord.ext import commands
import discord

from Wrappers.player import Player


class Binder(commands.Cog):  # TODO: finish it
    player_list = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bind(self, ctx, username: Union[discord.Member, str], guild_name: str, highest_lvl: int):
        player_name = Player(username)
        if not player_name.found:
            await ctx.channel.send(f'Player name \"{username}\" was not found')
            return

        if player_name['guild name'] != guild_name:
            await ctx.channel.send(f'Player \"{player_name}\" is not in guild \"{guild_name}\"')
            return

        await ctx.channel.send(str(player_name['highest level combat']))
        if player_name['highest level combat'] != highest_lvl:
            await ctx.channel.send(f'Highest level of player {player_name} is not {highest_lvl}')
            return

        Binder.player_list[ctx.author.id] = (username, player_name['guild name'])
        await ctx.channel.send(Binder.player_list)


def setup(bot):
    bot.add_cog(Binder(bot))
