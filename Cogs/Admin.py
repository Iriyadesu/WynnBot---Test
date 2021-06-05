"""
Module for a class containing commands for admins and converter from AuditlogAction -> str
"""
__all__ = [
    'Admin',
    'setup'
]

import logging
import json

import discord
from discord.ext import commands

import bot_data as bd
import util


class Admin(commands.Cog):
    """
    Class for admin commands
    """
    description_ = 'Admin commands'

    def __init__(self, bot: util.CustomBot):
        self.bot = bot

    @commands.command(usage='audit <get|retrieve>',
                      description='Command for getting and saving audit log')
    @commands.has_permissions(administrator=True)
    async def audit(self, ctx: commands.Context, option: str = 'save'):
        """
        Command for getting and saving audit log
        Actions:
        - get = sends audit log file
        - save = saves audit log (default)
        :param ctx: context of the message
        :param option: action to take
        :return: None
        """
        if option.lower() == 'save':  # save entries to file
            new_entries_list, audit_ids, new_entries_count = await _save_audit_log(
                ctx.guild.audit_logs(limit=None, oldest_first=True)
            )

            with open('data/audit_IDs.json', 'w') as file:  # save entry IDs
                file.write(json.dumps(audit_ids))

            with open('data/audit_log.txt', 'a') as file:  # add new entries
                for entry in new_entries_list:
                    file.write(f'{"-" * 32}')
                    file.write(json.dumps(entry, indent=2))

            await ctx.send(embed=discord.Embed(  # report success
                title='Success', description=f'Saved {new_entries_count} entries'))
            logging.info(f'Saved {new_entries_count} entries')

        elif option.lower() == 'retrieve':  # send log file
            with open('data/audit_log.txt', 'rb') as file:
                await ctx.send(file=discord.File(file, 'audit_log.txt'))

        else:
            raise util.UnknownArgumentException('Unknown parameter passed')

    @commands.command(usage='prefix <new prefix>',
                      description='change prefix of the bot')
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, prefix: str):
        """
        Command for changing bot's prefix

        :param ctx: context of the message
        :param prefix: prefix to change to
        :return: None
        """
        self.bot.config['prefix'] = prefix
        util.set_config(self.bot, self.bot.config)

        await ctx.send(embed=discord.Embed(
            colour=bd.embed_colors['info'],
            title='Success!',
            description=f'Successfully set bot prefix to \"{prefix}\"'
        ))


async def _save_audit_log(entries) -> tuple[list[dict], list[int], int]:
    """
    Helper function for getting audit log entries for saving
    :param entries: async iterator of audit log entries
    :return: list of new entries; list of new entry IDs; number of new entries
    """
    with open('data/audit_IDs.json', 'r') as file:  # get know entries (to prevent duplicates)
        audit_ids = json.loads(file.read())

    new_entries_list = []
    new_entries_count = 0
    async for entry in entries:  # iterate through entry list
        if entry.id in audit_ids:  # if it is already saved, skip
            continue
        new_entries_count += 1

        extra = '\n-- '.join(f'{key}: {value}' for key, value in entry.extra.items()) \
            if (entry.extra and isinstance(entry.extra, dict)) \
            else ''  # format extra attributes

        entry_dict = {  # information to save
            'action': bd.audit_action_converter[entry.action],  # type of action
            'user': entry.user.name + '#' + entry.user.discriminator,  # author of the action
            'date': entry.created_at.strftime('%Y/%m/%d %H:%M:%S'),  # when it was done
        }
        # ----- not to save unneeded info
        if entry.reason is not None:
            entry_dict['reason'] = entry.reason  # why it was done (usually None)
        before = _get_diff_dict(entry.before)
        after = _get_diff_dict(entry.after)
        if before:
            entry_dict['before'] = before  # difference
        if after:
            entry_dict['after'] = after
        if extra:
            entry_dict['extra'] = extra

        audit_ids.append(entry.id)  # mark entry as known
        new_entries_list.append(entry_dict)

    return new_entries_list, audit_ids, new_entries_count


def _get_diff_dict(entry) -> dict:
    """
    Helper function for getting info data into python dict
    :param entry: Audit log entry "before/after" attribute
    :return: dictionary of evaluated attributes
    """
    dc = {}
    for attr, val in entry:
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], discord.Role):  # if roles changed
            val = [role.name for role in val]
        elif not (val is None or isinstance(val, str)):  # if it can't be serialised into JSON
            val = repr(val)

        dc[attr] = val

    return dc


def setup(bot: util.CustomBot):
    """
    Add the "Events" class to the bot
    """
    bot.add_cog(Admin(bot))
