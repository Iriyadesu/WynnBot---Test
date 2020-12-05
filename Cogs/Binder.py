from discord.ext import commands

from Wrappers.player import Player
from bot_data import error_embed


class Binder(commands.Cog):  # TODO: finish it
    player_list = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bind(self, ctx, username: str, guild_name: str, highest_lvl: int):
        if ctx.author.id in Binder.player_list:
            await ctx.channel.send(
                embed=error_embed('user error',
                                  description=f'User {ctx.author.mention} is already bound'))
            return

        player_name = Player(username)
        if not player_name.found:
            await ctx.channel.send(
                embed=error_embed('user error',
                                  description=f'Player name \"{username}\" does not exist'))
            return

        if player_name['guild name'] != guild_name:
            await ctx.channel.send(
                embed=error_embed('user error',
                                  description=f'Player \"{username}\" is not in guild \"{guild_name}\"'))
            return

        if player_name['highest level combat'] != highest_lvl:
            await ctx.channel.send(
                embed=error_embed('user error',
                                  description=f'Highest level of {username} is not \"{highest_lvl}\"'))
            return

        Binder.player_list[ctx.author.id] = (username, player_name['guild name'], highest_lvl)
        await ctx.channel.send(Binder.player_list)


def setup(bot):
    bot.add_cog(Binder(bot))
