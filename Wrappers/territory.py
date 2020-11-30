from requests import get


class Territory:
    """
    Class containing all information for Wynncraft territory (1.19)
    """
    def __init__(self, name: str):
        """
        1) gets data
        2) checks for errors (codes 400, 429, anything except 200)
        3) decodes json and assigns data to 'data' variable
        5) creates dictionary containing all data
        """
        # sends request
        res = get('https://api.wynncraft.com/public_api.php?action=territoryList')

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

        data = jres['territories']
        if name not in data:
            self.found = None
            return
        else:
            self.found = True
        terr = data[name]

        self._data = {
            'name': name,
            'owner': terr['guild'],
            'acquired': terr['acquired'],
            'location': {
                'startX': terr['location']['startX'],
                'startZ': terr['location']['startY'],
                'endX': terr['location']['endX'],
                'endZ': terr['location']['endY']
            }
        }

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
            raise KeyError(f'Property \"{key}\" was not found in {self["name"]}')

    def __repr__(self):
        return f'<territory {self["name"]}>'
