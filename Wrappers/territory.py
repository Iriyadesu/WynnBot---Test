from typing import Union

import requests as r


def territory(name: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    3) decodes json and assigns data to 'data' variable
    5) creates dictionary containing all data
    """
    # sends request
    res = r.get('https://api.wynncraft.com/public_api.php?action=territoryList')

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
        res_data = res.json()['territories']

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
