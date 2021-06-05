"""
This module should contain all data used by the bot
Currently contains:
- colors
- error embed function
- help embed = not sure whether it is used
- nono words
"""

__all__ = [
    'colors',
    'embed_colors',
    'bad_words',
    'bad_words_list',
    'audit_action_converter'
]

from discord import AuditLogAction

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
    'normal': 0x00FF00,  # green
    'technical': 0xBCC0C0  # light grey
}


bad_words = {  # What words are to be moderated
    'minor': ('shit',),
    'mid': ('fuck', 'idiot', 'asshole'),
    'major': ('nigga', 'nigger', 'banboos')
}
bad_words_list = []  # create empty list
[bad_words_list.extend(category) for category in bad_words.values()]  # add all of the words to the list
bad_words_list = tuple(bad_words_list)  # make it a tuple

audit_action_converter = {  # Converting enum to string
    AuditLogAction.guild_update: 'Guild update',
    AuditLogAction.channel_create: 'Channel create',
    AuditLogAction.channel_update: 'Channel update',
    AuditLogAction.channel_delete: 'Channel delete',
    AuditLogAction.overwrite_create: 'Create overwrite',
    AuditLogAction.overwrite_update: 'Update overwrite',
    AuditLogAction.overwrite_delete: 'Delete overwrite',
    AuditLogAction.kick: 'Kick member',
    AuditLogAction.member_prune: 'Prune members',
    AuditLogAction.ban: 'Ban member',
    AuditLogAction.unban: 'Unban member',
    AuditLogAction.member_update: 'Update member',
    AuditLogAction.member_role_update: 'Update member roles',
    AuditLogAction.member_move: 'Move member',
    AuditLogAction.member_disconnect: 'Disconnect member',
    AuditLogAction.bot_add: 'Add bot',
    AuditLogAction.role_create: 'Create role',
    AuditLogAction.role_update: 'Update role',
    AuditLogAction.role_delete: 'Delete role',
    AuditLogAction.invite_create: 'Create invite',
    AuditLogAction.invite_update: 'Update invite',
    AuditLogAction.invite_delete: 'Delete invite',
    AuditLogAction.webhook_create: 'Create webhook',
    AuditLogAction.webhook_update: 'Update webhook',
    AuditLogAction.webhook_delete: 'Delete webhook',
    AuditLogAction.emoji_create: 'Create emoji',
    AuditLogAction.emoji_update: 'Update emoji',
    AuditLogAction.emoji_delete: 'Delete emoji',
    AuditLogAction.message_delete: 'Delete message',
    AuditLogAction.message_bulk_delete: 'Delete message bulk',
    AuditLogAction.message_pin: 'Pin message',
    AuditLogAction.message_unpin: 'Unpin message',
    AuditLogAction.integration_create: 'Create integration',
    AuditLogAction.integration_update: 'Update integration',
    AuditLogAction.integration_delete: 'Delete integration',
}
