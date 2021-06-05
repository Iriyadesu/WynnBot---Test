"""
Utility function for Wynncraft API wrappers
"""
__all__ = [
    'api_call'
]

from typing import Union, Dict

import requests as r


# TODO: Try to find a way to move params here for v2
def api_call(api_version: str, params: Union[Dict[str, str], str]) -> Union[dict, None]:
    """
    1) gets data
    2) checks for errors (codes 400, 429, anything except 200)
    2a) if the player was not found (code 400) return None
    3) decodes json and assigns data to 'data' variable
    5) returns dictionary containing all data

    :param api_version: either "legacy" or "v2"
    :param params: additional parameters of the request; url for v2
    """
    # sends request
    if api_version == 'legacy':
        response = r.get('https://api.wynncraft.com/public_api.php', params=params)
    else:
        response = r.get('https://api.wynncraft.com/v2/' + params)

    # status codes
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
