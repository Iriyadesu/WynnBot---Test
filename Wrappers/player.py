
"""
Class 'Player' info:

All information can be accessed by self[key] where 'self' is instance of Player and key is string.

All valid keys
keys : returned value
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


Class 'WClass' info:

All information can be accessed by self[key] where 'self' is instance of Player and key is string.

All valid keys
key  : returned value
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
skills : dictionary containing player's skill; valid keys: strength, STR, dexterity, DEX, intelligence, INT, defense, DEF, agility, AGI
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

from requests import get


# noinspection PyTypeChecker
class Player:
    """
    Class containing all information for Wynncraft player
    """
    def __init__(self, name: str):
        """
        1) gets data
        2) checks for errors (codes 400, 429, anything except 200)
        3) decodes json and assigns data to 'data' variable
        4) creates _name and _uuid attributes
        5) creates dictionary containing all data
        """
        # sends request
        res = get(f'https://api.wynncraft.com/v2/player/{name}/stats')

        if res.status_code == 400:
            # if status code is 400 (non-existing name)
            raise NameError(f'name was not found')

        elif res.status_code == 429:
            # if too many requests are sent (exceeded the limit)(750/30min/ip)
            raise Exception('Too many requests!')

        elif res.status_code != 200:
            # other errors
            raise Exception(f'Cannot procede. Status code: {res.status_code}')

        else:
            # status code is 200

            # gets the json
            jres = res.json()
            self._name = name
            self._uuid = jres['data'][0]['uuid']

        data = jres['data'][0]
        
        rank = data['rank'] if data['rank'] != 'Player' else 'Normal'
        location = data['meta']['location']['server'] if data['meta']['location']['online'] is not False else None
        
        self._data = {
            # meta
            'username': data['username'],
            'position': rank if rank != 'Normal' else 'Player',
            'rank': data['meta']['tag']['value'],
            'veteran': data['meta']['veteran'],
            'total playtime': int(data['meta']['playtime']/60*4.7),  # matches web stats, idk why is it that
            'location': location,
            'first join': data['meta']['firstJoin'],
            'last join': data['meta']['lastJoin'],
            # guild
            'guild name': data['guild']['name'],
            'guild rank': data['guild']['rank'],
            # global
            'chests found': data['global']['chestsFound'],
            'mobs killed': data['global']['mobsKilled'],
            'total level combat': data['global']['totalLevel']['combat'],
            'total level professions': data['global']['totalLevel']['profession'],
            'total level combined': data['global']['totalLevel']['combined'],
            'logins': data['global']['logins'],
            'deaths': data['global']['deaths'],
            'pvp kills': data['global']['pvp']['kills'],
            'pvp deaths': data['global']['pvp']['deaths'],
            'classes': [WClass(cls, self._name) for cls in data['classes']]
            }

        highestlvl = 0
        for player_class in self._data['classes']:
            if player_class['combat level'] > highestlvl:
                highestlvl = player_class['combat level']
        self._data['highest level combat'] = highestlvl

    def update(self):
        """Updates the information. Basically it initialises itself again."""
        self.__init__(self._uuid)
    
    def __getitem__(self, key):
        """
        Allows to access data by doing object[key].
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('Player %s doesn't have \'%s\' stat' %(self['username'], key))
        """

        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f'Player {self["username"]} doesn\'t have \'{key}\' stat')

    def __repr__(self):
        return f'<{self["position"]} {self._name}>'


class WClass:
    """
    Class for containing information of player's classes
    """
    def __init__(self, data, owner):

        self._owner = owner
        clss = ['archer', 'hunter',
                'assassin', 'ninja',
                'mage',
                'warrior', 'knight',
                'shaman', 'skyseer']

        cdata = {}

        # class
        self._name = data['name']
        for j in clss:
            if j in data['name']:
                cdata['class'] = j
                break
            elif 'darkwizard' in data['name']:
                cdata['class'] = 'dark wizard'
                break

        # stats (general)
        cdata['chests found'] = data['chestsFound']
        cdata['mob killed'] = data['mobsKilled']
        cdata['gamemodes'] = data['gamemode']
        cdata['playtime'] = data['playtime']
        cdata['logins'] = data['logins']
        cdata['deaths'] = data['deaths']

        cdata['pvp kills'] = data['pvp']['kills']
        cdata['pvp kills'] = data['pvp']['deaths']

        cdata['quests completed'] = data['quests']['completed']
        cdata['quests list'] = data['quests']['list']

        # skills
        skills = {
                  'STR': data['skills']['strength'],
                  'DEX': data['skills']['dexterity'],
                  'INT': data['skills']['intelligence'],
                  'DEF': data['skills']['defense'],
                  'AGI': data['skills']['agility'],
                  **data['skills'],
                  }
        cdata['skills'] = skills
        del cdata['skills']['defence']
        
        # stats (combat and profession)
        cdata['total level'] = data['level']
        
        cdata['combat level'] = data['professions']['combat']['level']
        cdata['woodcutting level'] = data['professions']['woodcutting']['level']
        cdata['mining level'] = data['professions']['mining']['level']
        cdata['fishing level'] = data['professions']['fishing']['level']
        cdata['farming level'] = data['professions']['farming']['level']
        cdata['alchemism level'] = data['professions']['alchemism']['level']
        cdata['armouring level'] = data['professions']['armouring']['level']
        cdata['cooking level'] = data['professions']['cooking']['level']
        cdata['jeweling level'] = data['professions']['jeweling']['level']
        cdata['scribing level'] = data['professions']['scribing']['level']
        cdata['tailoring level'] = data['professions']['tailoring']['level']
        cdata['weaponsmithing level'] = data['professions']['weaponsmithing']['level']
        cdata['woodworking level'] = data['professions']['woodworking']['level']

        cdata['combat xp'] = data['professions']['combat']['xp']
        cdata['woodcutting xp'] = data['professions']['woodcutting']['xp']
        cdata['mining xp'] = data['professions']['mining']['xp']
        cdata['fishing xp'] = data['professions']['fishing']['xp']
        cdata['farming xp'] = data['professions']['farming']['xp']
        cdata['alchemism xp'] = data['professions']['alchemism']['xp']
        cdata['armouring xp'] = data['professions']['armouring']['xp']
        cdata['cooking xp'] = data['professions']['cooking']['xp']
        cdata['jeweling xp'] = data['professions']['jeweling']['xp']
        cdata['scribing xp'] = data['professions']['scribing']['xp']
        cdata['tailoring xp'] = data['professions']['tailoring']['xp']
        cdata['weaponsmithing xp'] = data['professions']['weaponsmithing']['xp']
        cdata['woodworking xp'] = data['professions']['woodworking']['xp']

        # dungeons
        cdata['total dungeons'] = data['dungeons']['completed']
        
        ddict = {
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
                dungeons[ddict[j['name']]] = j['completed']
            except KeyError:
                pass

        cdata['dungeons'] = dungeons

        self._data = cdata

    def __getitem__(self, key):
        """
        Allows to access data by doing object[key].
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('Player %s doesn't have \'%s\' stat' %(, key))
        """
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f'Player\'s class \'{self._name}\' doesn\'t have \'{key}\' stat')

    def __repr__(self):
        return f'<{self._owner}\'s {self["class"]}; combat lv.{self["combat level"]}>'
