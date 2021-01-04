"""
uh
"""
from typing import Union

import requests as r


def guild(name: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    2a) if the player was not found (code 400) return None
    3) decodes json and assigns data to 'data' variable
    5) returns dictionary containing all data
    """
    # sends request
    res = r.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={name}')

    if res.status_code == 400:
        # if status code is 400 (non-existing name)
        return

    elif res.status_code == 429:
        # if too many requests are sent (exceeded the limit)(750/30min/ip)
        raise Exception('Too many requests!')

    elif res.status_code != 200:
        # other errors
        raise Exception(f'Cannot proceed. Status code: {res.status_code}')

    else:
        # status code is 200
        # gets the json
        if 'error' in res.json():  # weird api thing; on error returns code 200
            return
        res_data = res.json()

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
