"""
uh
"""
from typing import Union

from Wrappers.__init__ import api_call


def guild(name: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    2a) if the player was not found (code 400) return None
    3) decodes json and assigns data to 'data' variable
    5) returns dictionary containing all data
    """
    # sends request
    res_data = api_call(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={name}')
    if res_data is None:  # if not found
        return

    guild_data = {
        'name': res_data['name'],
        'prefix': res_data['prefix'],
        'level': res_data['level'],
        'xp': res_data['xp'],
        'created': res_data['created'],
        'created friendly': res_data['createdFriendly'],
        'territories': res_data['territories'],
        'banner tier': res_data['banner']['tier'],
        'banner': res_data['banner'],
        'members': [_guild_member(member) for member in res_data['members']]
    }

    return guild_data


def _guild_member(data: dict) -> dict:
    """
    Helper function, will be probably removed
    """
    data['joined friendly'] = data['joinedFriendly']
    del data['joinedFriendly']

    return data
