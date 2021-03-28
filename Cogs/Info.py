import bot_data as bd

from discord.ext import commands
import discord


class Info(commands.Cog):
    """
    This class handles informational commands
    """

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(description="TOD0 list", usage="!todo")
    async def todo(self, ctx):
        embed = discord.Embed(title='TODO:', color=bd.embed_colors['info'])
        embed.add_field(name='todo', value=bd.todo_str)

        await ctx.send(embed=embed)

    @commands.command(aliases=['commands', 'command'],
                      usage="!help [cog]", description="displays this message")
    async def help(self, ctx: commands.Context, cog='all'):
        embed = discord.Embed(
            title='Help', color=bd.embed_colors['info'])
        embed.set_thumbnail(url=bd.embed_thumbnail)
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url)

        # Get a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]
        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            for cog in cogs:
                if cog != "Events":  # We don't want "on_message" etc. show up

                    # Get a list of all commands under each cog
                    commands_list = ""
                    for command in self.bot.get_cog(cog).get_commands():
                        commands_list += f'**{command.name}**: *{command.usage}* *=* *{command.description}*\n'
                    # Add the cog's details to the embed.
                    embed.add_field(
                        name=f'__{cog}__',
                        value=(commands_list if commands_list else 'none'),  # Prevents bug when a cog has no commands
                        inline=False)
            await ctx.send(embed=embed)

        else:  # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]

            if not cog.lower() in lower_cogs or cog.lower() == 'events':  # If the cog doesn't exists.
                await ctx.send(
                    embed=bd.error_embed('Human error', 'Invalid cog specified.\nUse `help` command to list all cogs.')
                )

            else:
                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[lower_cogs.index(cog.lower())]).get_commands()

                help_text = f'__{cog}:__\n' + '\\_' * 32 + '\n'
                for command in commands_list:
                    help_text += f'__{command.name}__\n'
                    help_text += f'Description: {command.description}\n'

                    if len(command.aliases) > 0:  # Also add aliases, if there are any
                        help_text += f'Aliases: `{"`, `".join(command.aliases)}`\n'

                    # Finalise the cog help
                    help_text += f'Usage: `{command.usage if command.usage is not None else ""}`\n'

                embed.description = help_text

                await ctx.send(embed=embed)  # send it

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Command for checking latency

        :param ctx: channel where the command was used
        :return: None
        """
        await ctx.send(f'Latency is {self.bot.latency*1000:.3f}ms')


def setup(bot: commands.Bot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Info(bot))
