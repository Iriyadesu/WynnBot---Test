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
    res_data = api_call('legacy', {'action': 'territoryList'})
    if res_data is None:  # if not found
        return

    if name not in res_data['territories']:
        return

    return res_data['territories'][name]
