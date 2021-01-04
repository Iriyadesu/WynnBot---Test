from typing import Union

from Wrappers.__init__ import api_call


def territory(name: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    3) decodes json and assigns data to 'data' variable
    5) creates dictionary containing all data
    """
    # sends request
    res_data = api_call('https://api.wynncraft.com/public_api.php?action=territoryList')
    if res_data is None:  # if not found
        return

    # res_data = res.json()['territories']

    if name not in res_data:
        return

    terr = res_data[name]

    territory_data = {
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
    return territory_data
