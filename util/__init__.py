"""
Package for utility functions for the bot
"""
__all__ = [
    'load_config',
    'set_config',
    'error_embed',
    'file_attachment_to_str',
    'determine_prefix',
    'check_conditions'
]

import json
import logging
from typing import Any, Union

import discord
from discord.ext import commands

import bot_data as bd


class CustomBot(commands.Bot):
    """
    Subclass of Bot class to automatically make "config" field.
    Also to make the IDE not to complain
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()


def load_config(path: str = 'config.json') -> dict[str, Any]:
    """
    Function for loading configuration from a file
    :param path: path to the config file
    :return: config
    """
    with open(path, 'r') as file:
        return json.loads(file.read())


def set_config(bot: CustomBot, config: str, path: str = 'config.json'):
    """
    Function for saving (not applying) configuration to a file
    :param bot: bot whose config is changed
    :param config: config to be saved
    :param path: path to the config file
    """
    with open(path, 'w') as file:
        file.write(json.dumps(config, indent=2))

    bot.config = config  # load the new config into the bot (doesn't apply the stuff though)


def error_embed(err_type: str = 'No reason provided', description: str = None, usage=None) -> discord.Embed:
    """
    Returns embed for errors

    :param err_type: type of the error
    :param description: description of the embed
    :param usage: usage of the command
    :return: discord.Embed
    """
    embed = discord.Embed(title='Error!',
                          color=bd.embed_colors['error'],
                          description='An Error occurred during processing of the command')
    embed.add_field(name='Type:' if description is not None else 'Reason:', value=err_type, inline=False)
    if description is not None:
        embed.add_field(name='Reason:', value=description, inline=True)
    if usage is not None:
        embed.add_field(name='Command usage:', value=usage)

    return embed


class UnknownArgumentException(commands.BadArgument):
    """Exception for unknown arguments for commands"""
    pass


async def file_attachment_to_str(attachment: discord.Attachment) -> str:
    """
    Function for converting attachment file to string
    :param attachment: discord attachment to be converted
    :return: file's content
    """
    if not _is_plain_text(attachment.content_type):  # if it is not plain text (NOTE: Might not support.js files)
        raise TypeError('Attachment type must be plain text')

    return ''.join(map(
        chr,  # yields int --> convert to char
        await attachment.read()  # get attachment's text
    ))


def _is_plain_text(typ: str) -> bool:
    """
    Helper function for determining whether the attachment is a plain-text file
    The type looks like "application/xml; charset=utf-8", where "application/xml" is the only relevant bit

    TODO: Add types as they are encountered
    :param typ: type of the attachment
    :return: whether it is plain-text file or not
    """
    application = ['application/' + app_typ for app_typ in ('json', 'javascript', 'xml', 'x-sql')]
    if not any((app_typ not in typ) for app_typ in application):  # files also used for other stuff (still plain-text)
        return True

    if 'text' in typ:  # plain text files
        return True

    return False


async def determine_prefix(bot: CustomBot, message: discord.Message) -> list[str]:
    """
    Function allowing dynamically change bot prefix
    :param bot: bot whose prefix is to change
    :param message: message used to determine the new prefix; unused
    :return: list of prefixes
    """
    return [f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ', bot.config['prefix']]


def check_conditions(*conditions: tuple[bool, str]) -> Union[str, bool]:
    """
    Helper function for checking a series of conditions and returning error message on failure
    :param conditions: conditions to check
    :return: either True or failure string
    """
    for condition in conditions:
        if not condition[0]:  # condition is false return error message
            return condition[1]

    return True


def log_print(string: str, level: str = 'INFO'):
    """
    Function for printing and logging a string

    :param level: level of the logging
    :param string: string to print and log
    """
    logging.log(logging.getLevelName(level), string)
    print(string)


def get_cog_name_list(bot: discord.ext.commands.Bot):
    """
    :param bot: bot instance
    :return: list of the names of all cogs except "Events"
    """
    return list(filter(lambda x: x != 'Events', bot.cogs.keys()))
