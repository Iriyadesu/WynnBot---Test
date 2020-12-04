from discord.ext import commands
import discord


class Binder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bind(self, ctx, username):
        await ctx.channel.send(username)


def setup(bot):
    bot.add_cog(Binder(bot))
