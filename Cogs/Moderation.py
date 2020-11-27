from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
     #  ----- ban -----
    @commands.command(description="Bans someone")
    async def ban(self,ctx, user: discord.Member, *, reason="No reason provided"):
            await user.ban(reason=reason)
            ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
            await ctx.message.delete()
            await ctx.channel.send(embed=ban)
            await user.send(embed=ban)
    # ----- kick -----
    @commands.command(description="kicks someone")
    async def kick(self,ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        ban = discord.Embed(title=f":boom: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)

def setup(bot):
    bot.add_cog(Moderation(bot))