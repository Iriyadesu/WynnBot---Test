from discord.ext import commands
import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #  ----- ban -----
    @commands.command(description="Bans someone")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban_embed = discord.Embed(title=f":boom: Banned {user.name}!",
                                  description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                  color=0xCCCC00)
        await ctx.message.delete()
        await ctx.channel.send('Seems like you were not behaving properly.\n Next', embed=ban_embed)
        await user.send(embed=ban_embed)

    # ----- kick -----
    @commands.command(description="kicks someone")
    #@commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick_embed = discord.Embed(title=f":boom: Kicked {user.name}!",
                                   description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                                   color=0xCCCC00)
        await ctx.message.delete()
        await ctx.channel.send(embed=kick_embed)
        kick_embed.title = 'You were kicked!'
        await user.send('Seems like you were not behaving properly.\nNext please do not break the rules',
                        embed=kick_embed)

    # ----- repeat -----
    @commands.command(description="speak beep boop")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg="Nothing"):
        try: 
            await ctx.channel.send(str(arg))
        except Exception as e:
            await ctx.channel.send('Cannot assign role. Error: ' + str(e))


def setup(bot):
    bot.add_cog(Moderation(bot))
