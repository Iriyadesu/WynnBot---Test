"""
Wrappers for "player" requests

TO-DO: Check at some point again
"""

from typing import Dict, Any, Optional

from Wrappers.__init__ import api_call


def player(name: str) -> Optional[Dict[str, Any]]:
    """
    Wrapper for "player" requests.

    Changed from raw response:
    - "meta" and "global" object we unpacked into main dict
    - 'rank' is player's rank (VIP/VIP+/HERO/champion)
    - 'position' is player's position (Player/Admin/Moderator/GM etc.)
    - 'highestLvlCombat' is player's highest combat level on a class
    - 'location' is None if player is offline or world where the player is
    - 'playtime' was changed to match Wynn's stats ('playtimeRaw' has it directly from API)
    - 'skills' and 'dungeons' in 'classes' have acronyms in addition to original keys

    :param name: name of requested player
    :return: if found: dict of player's data; else None
    """
    data = api_call('v2', f'player/{name}/stats')
    if data is None:  # if not found
        return
    data = data['data'][0]

    location = data['meta']['location']['server'] if data['meta']['location']['online'] is not False else None
    highest_level = 0  # afaik not in API
    for player_class in data['classes']:
        try:
            if player_class['professions']['combat']['level'] > highest_level:
                highest_level = player_class['professions']['combat']['level']
        except KeyError as ke:  # sometimes it is just None...
            print(f'{"-"*16}\nKeyError on highest level calculation\nKey: {ke}\n{"-"*16}')

    data_final = {
        'username': data['username'],
        'uuid': data['uuid'],
        'position': data['rank'],  # Position as Admin, Mod, GM etc.

        **data['meta'],
        'rank': data['meta']['tag']['value'],  # rank as VIP/VIP+/HERO/champion
        'playtime': int(data['meta']['playtime'] / 60 * 4.7),  # this one stat is WEIRD
        'playtimeRaw': data['meta']['playtime'],
        'location': location,
        'highestLvlCombat': highest_level,

        'guild': data['guild'],  # left it as it is from API
        **data['global'],  # only unzipped it
        'ranking': data['ranking'],  # no idea what do do with it as of now
        'classes': [_player_class(class_data) for class_data in data['classes']]
    }
    del data_final['tag']

    return data_final


def _player_class(data: dict) -> Dict[str, Any]:
    """
    Function to prepare class dat

    :param data: data of the class
    :return: formatted data of the class
    """
    # currently, removed dungeons are not supported
    dungeon_dict = {  # dict for adding acronyms to dungeon dict
        'Decrepit Sewers': 'DS',
        'Infested Pit': 'IP',
        'Lost Sanctuary': 'LS',
        'Underworld Crypt': 'UC',
        'Sand-Swept Tomb': 'SST',
        'Ice Barrows': 'IB',
        'Undergrowth Ruins': 'UR',
        'Galleon\'s Graveyard': 'GG',
        'Fallen Factory': 'FF',
        'Eldritch Outlook': 'EO',
        'Corrupted Decrepit Sewers': 'CDS',
        'Corrupted Infested Pit': 'CIP',
        'Corrupted Lost Sanctuary': 'CLS',
        'Corrupted Underworld Crypt': 'CUC',
        'Corrupted Sand-Swept Tomb': 'CSST',
        'Corrupted Ice Barrows': 'CIB',
        'Corrupted Undergrowth Ruins': 'CUR',
    }

    dungeons = {
        'completed': data['dungeons']['completed']
    }
    for j in data['dungeons']['list']:
        try:
            dungeons[j['name']] = j['completed']  # as in API
            dungeons[dungeon_dict[j['name']]] = j['completed']  # acronyms
        except KeyError:
            pass

    skills = {
        'STR': data['skills']['strength'],  # acronyms
        'DEX': data['skills']['dexterity'],
        'INT': data['skills']['intelligence'],
        'DEF': data['skills']['defense'],
        'AGI': data['skills']['agility'],
        **data['skills']  # as in API
    }

    # everything from original data
    data['dungeons'] = dungeons  # customised dungeons
    data['skills'] = skills  # customised skills

    return data


def player_raw(name: str) -> Optional[Dict[str, Any]]:
    """
    Returns raw response.

    :param name: name of requested player
    :return: if found: dict obtained from response; else None
    """
    return api_call('v2', f'/player/{name}/stats')


"""
class_names = [
    'archer', 'hunter',
    'assassin', 'ninja',
    'mage',
    'warrior', 'knight',
    'shaman', 'skyseer'
]
"""
