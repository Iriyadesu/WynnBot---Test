"""
uh
"""

from requests import get


class Guild:
    """
    Class containing all information about a guild
    """
    def __init__(self, name: str):
        res = get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command={name}')
        data = res.json()

        self._data = {
            'name': data['name'],
            'prefix': data['prefix'],
            'level': data['level'],
            'xp': data['xp'],
            'created': data['created'],
            'territories': data['territories'],
            'banner tier': data['banner']['tier'],
            'banner': data['banner'],
            'members': [GMember(i, data['name']) for i in data['members']]
        }

    def update(self):
        """Updates the information. Basically it initialises itself again."""
        self.__init__(self['name'])

    def __getitem__(self, key):
        """
        Allows to access data by doing object[key].
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('Guild %s doesn't have \'%s\' stat' %(self['username'], property))
        """
        try:
            # print(self.data[key])
            return self._data[key]
        except KeyError:
            raise KeyError(f'Guild {self["name"]} doesn\'t have \'{key}\' property')

    def __repr__(self):
        return f'<Guild {self["name"]}>'


class GMember:
    """
    Class containing all information about guild member
    """
    def __init__(self, data, owner):
        print(data, owner)

        self._owner = owner
        self._data = data

        self._data['joined friendly'] = self._data['joinedFriendly']
        del self._data['joinedFriendly']

    def __getitem__(self, key):
        """
        Allows to access data by doing object[key].
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('Guild %s doesn't have \'%s\' stat' %(self['username'], property))
        """
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f'Guild member of {self["name"]} doesn\'t have \'{key}\' property')

    def __repr__(self):
        return f'<{self["name"]}, {self["rank"]} of {self._owner}>'


if __name__ == '__main__':
    g = Guild('BOOF')
    print(g['memberso'])
