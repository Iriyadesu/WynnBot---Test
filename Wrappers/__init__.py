"""
Contains API wrappers for the Wynncraft cog
"""
from typing import Union

import requests as r


# TODO: Once API is updated redo the wrappers (namely: player, guild).
#  Currently it is just stupid


def api_call(url: str) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    2a) if the player was not found (code 400) return None
    3) decodes json and assigns data to 'data' variable
    5) returns dictionary containing all data
    """
    # sends request
    response = r.get(url)

    if response.status_code == 400:
        # if status code is 400 (non-existing name or not found)
        return

    elif response.status_code == 429:
        # if too many requests are sent (exceeded the limit)(750/30min/ip)
        raise Exception('Too many requests!')

    elif response.status_code != 200:
        # other errors
        raise Exception(f'Cannot proceed. Status code: {response.status_code}')

    else:
        # status code is 200
        # gets the json
        res_data = response.json()

        return res_data
