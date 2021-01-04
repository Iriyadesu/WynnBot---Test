
"""

Dict returned by "player" function:
All valid keys:
keys : returned value (type)
--------------------
- username : username (str)
- position : position (str; default is Normal; e.g. Admin, Moderator, Media etc.)
- rank : donor rank (str; VIP/VIP+/HERO)
- veteran : (boolean)
- total playtime : total playtime synced with web (int; not very accurate)
- location : server/None (str/None; if the player is online, returns server, else None)
- first join : (str) 2017-05-17T13:48:19.352Z
- last join : 2020-08-13T11:11:56.602Z
- guild name : guild name/None (str/None)
- guild rank : guild rank/None (str/None)
- guild : instance of Guild class
- chests found : (int)
- mobs killed : (int)
- total level combat : (int)
- total level professions : (int)
- total level combined : (int)
- logins : (int)
- deaths : (int)
- pvp kills : (int)
- pvp deaths : (int)
- classes : list of WClass instances

Classes:
All valid keys
key  : returned value (type)
--------------------
class : class type (str)
chests found : (int)
mob killed : (int)
gamemodes : dictionary; valid keys: hardcore, ironman, craftsman 
playtime : (int)
logins : (int)
deaths : (int)
pvp kills : (int)
quests completed : (int)
quests list : list of completed quests
skills : dictionary containing player's skill; valid keys:
    -strength, STR, dexterity, DEX, intelligence, INT, defense, DEF, agility, AGI
total level : (int)
combat level : (int)
woodcutting level : (int)
mining level : (int)
fishing level : (int)
farming level : (int)
alchemism level : (int)
armouring level : (int)
cooking level : (int)
jeweling level : (int)
scribing level : (int)
tailoring level : (int)
weaponsmithing level : (int)
woodworking level : (int)
combat xp : (float, in %)
woodcutting xp : (float, in %)
mining xp : (float, in %)
fishing xp : (float, in %)
farming xp : (float, in %)
alchemism xp : (float, in %)
armouring xp : (float, in %)
cooking xp : (float, in %)
jeweling xp : (float, in %)
scribing xp : (float, in %)
tailoring xp : (float, in %)
weaponsmithing xp : (float, in %)
woodworking xp : (float, in %)
total dungeons : (int)
dungeons : dictionary; valid keys: DS, IP, IB, SST, LS, UR, UC, GG, CDS, CSST, FF, CIB, CLS, CIP, CUC, EO, CUR
"""
from typing import Union

import requests as r

from Wrappers.guild import guild


def player(name: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    2a) if the player was not found (code 400) return None
    3) decodes json and assigns data to 'data' variable
    5) returns dictionary containing all data
    """
    # sends request
    res = r.get(f'https://api.wynncraft.com/v2/player/{name}/stats')

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
        res_data = res.json()['data'][0]

    rank = res_data['rank'] if res_data['rank'] != 'Player' else 'Normal'
    location = res_data['meta']['location']['server'] if res_data['meta']['location']['online'] is not False else None

    player_data = {
        # meta
        'username': res_data['username'],
        'uuid': res_data['uuid'],
        'position': rank if rank != 'Normal' else 'Player',
        'rank': res_data['meta']['tag']['value'],
        'veteran': res_data['meta']['veteran'],
        'total playtime': int(res_data['meta']['playtime'] / 60 * 4.7),  # matches web stats, idk why is it that
        'location': location,
        'first join': res_data['meta']['firstJoin'],
        'last join': res_data['meta']['lastJoin'],
        # guild
        'guild instance': guild(res_data['guild']['name']),
        'guild name': res_data['guild']['name'],
        'guild rank': res_data['guild']['rank'],
        # global
        'chests found': res_data['global']['chestsFound'],
        'mobs killed': res_data['global']['mobsKilled'],
        'total level combat': res_data['global']['totalLevel']['combat'],
        'total level professions': res_data['global']['totalLevel']['profession'],
        'total level combined': res_data['global']['totalLevel']['combined'],
        'logins': res_data['global']['logins'],
        'deaths': res_data['global']['deaths'],
        'pvp kills': res_data['global']['pvp']['kills'],
        'pvp deaths': res_data['global']['pvp']['deaths'],
        'classes': [_player_class(cls, res_data['uuid']) for cls in res_data['classes']]
    }

    highest_level = 0
    for player_class in player_data['classes']:
        if player_class['combat level'] > highest_level:
            highest_level = player_class['combat level']
    player_data['highest level combat'] = highest_level

    return player_data


def _player_class(data: dict, owner: str) -> dict:
    _owner = owner
    class_names = ['archer', 'hunter',
                   'assassin', 'ninja',
                   'mage',
                   'warrior', 'knight',
                   'shaman', 'skyseer'
                   ]

    class_data = {}

    # class
    for j in class_names:
        if j in data['name']:
            class_data['class'] = j
            break
        elif 'darkwizard' in data['name']:
            class_data['class'] = 'dark wizard'
            break

    # stats (general)
    class_data['chests found'] = data['chestsFound']
    class_data['mob killed'] = data['mobsKilled']
    class_data['gamemodes'] = data['gamemode']
    class_data['playtime'] = data['playtime']
    class_data['logins'] = data['logins']
    class_data['deaths'] = data['deaths']

    class_data['pvp kills'] = data['pvp']['kills']
    class_data['pvp kills'] = data['pvp']['deaths']

    class_data['quests completed'] = data['quests']['completed']
    class_data['quests list'] = data['quests']['list']

    # skills
    skills = {
              'STR': data['skills']['strength'],
              'DEX': data['skills']['dexterity'],
              'INT': data['skills']['intelligence'],
              'DEF': data['skills']['defense'],
              'AGI': data['skills']['agility'],
              **data['skills'],
              }
    class_data['skills'] = skills
    del class_data['skills']['defence']

    # stats (combat and profession)
    class_data['total level'] = data['level']

    class_data['combat level'] = data['professions']['combat']['level']
    class_data['woodcutting level'] = data['professions']['woodcutting']['level']
    class_data['mining level'] = data['professions']['mining']['level']
    class_data['fishing level'] = data['professions']['fishing']['level']
    class_data['farming level'] = data['professions']['farming']['level']
    class_data['alchemism level'] = data['professions']['alchemism']['level']
    class_data['armouring level'] = data['professions']['armouring']['level']
    class_data['cooking level'] = data['professions']['cooking']['level']
    class_data['jeweling level'] = data['professions']['jeweling']['level']
    class_data['scribing level'] = data['professions']['scribing']['level']
    class_data['tailoring level'] = data['professions']['tailoring']['level']
    class_data['weaponsmithing level'] = data['professions']['weaponsmithing']['level']
    class_data['woodworking level'] = data['professions']['woodworking']['level']

    class_data['combat xp'] = data['professions']['combat']['xp']
    class_data['woodcutting xp'] = data['professions']['woodcutting']['xp']
    class_data['mining xp'] = data['professions']['mining']['xp']
    class_data['fishing xp'] = data['professions']['fishing']['xp']
    class_data['farming xp'] = data['professions']['farming']['xp']
    class_data['alchemism xp'] = data['professions']['alchemism']['xp']
    class_data['armouring xp'] = data['professions']['armouring']['xp']
    class_data['cooking xp'] = data['professions']['cooking']['xp']
    class_data['jeweling xp'] = data['professions']['jeweling']['xp']
    class_data['scribing xp'] = data['professions']['scribing']['xp']
    class_data['tailoring xp'] = data['professions']['tailoring']['xp']
    class_data['weaponsmithing xp'] = data['professions']['weaponsmithing']['xp']
    class_data['woodworking xp'] = data['professions']['woodworking']['xp']

    # dungeons
    class_data['total dungeons'] = data['dungeons']['completed']

    dungeon_dict = {
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

    dungeons = {}

    # currently, removed dungeons are not supported
    for j in data['dungeons']['list']:
        try:
            dungeons[dungeon_dict[j['name']]] = j['completed']
        except KeyError:
            pass

    return class_data
