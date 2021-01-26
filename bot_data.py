"""
This module should contain all data used by the bot
Currently contains:
- colors
- error embed function
- help embed = not sure whether it is used
- nono words
"""

import discord

# TODO: move here as much data as possible

colors = {
    'DEFAULT': 0x000000,
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'GREY': 0x95A5A6,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_GREY': 0x979C9F,
    'DARKER_GREY': 0x7F8C8D,
    'LIGHT_GREY': 0xBCC0C0,
    'DARK_NAVY': 0x2C3E50,
    'BLURPLE': 0x7289DA,
    'GREYPLE': 0x99AAB5,
    'DARK_BUT_NOT_BLACK': 0x2C2F33,
    'NOT_QUITE_BLACK': 0x23272A
}

embed_colors = {  # Colors used for specific embeds
    'info': 0x0000FF,  # blue
    'error': 0,  # black
    'moderation': 0xFFFF00,  # yellow
    'normal': 0x00FF00  # green
}

# thumbnail for embeds
embed_thumbnail = 'https://cdn.discordapp.com/attachments/776102426776305717/776530245066686505/Untitled_Artwork.png'

# String for "to-do" command
todo_str = """
TODO:
-? settings
-? - maybe for how much moderation do you want?
- maybe some moderation (f-words etc.)
-  -? levels of bad words. E.g. sh** would just log it, not remove the message, while f*** would do both
- bind user to MC account
- store all these things in JSON
- mute command - drastically improve it. Works, but badly
- test everything on our new friend
-! recheck documentation (both back- and front- end)
-! update API wrapper documentation
-? maybe add more Wynn API commands?
-? - like leaderboards etc
-! reorganise what is needed

WHEN DONE:
- uncomment perms requirements
"""

bad_words = {  # What words are to be moderated
    'minor': ('shit',),
    'mid': ('fuck', 'idiot', 'asshole'),
    'major': ('nigga', 'nigger')
}
bad_words_list = []  # create empty list
[bad_words_list.extend(category) for category in bad_words.values()]  # add all of the words to the list
bad_words_list = tuple(bad_words_list)  # make it a tuple


def error_embed(err_type: str = 'No reason provided', description: str = '') -> discord.Embed:
    """
    Returns embed for errors

    :param err_type: type of the error
    :param description: description of the embed
    :return: discord.Embed
    """
    embed = discord.Embed(title='Error!', description='An Error occurred during processing of the command')
    embed.add_field(name='Type:', value=err_type, inline=False)
    embed.add_field(name='Reason:', value=description)

    return embed
