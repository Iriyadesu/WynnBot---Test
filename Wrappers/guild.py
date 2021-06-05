"""
Wrappers for Wynncraft "guild" API
"""
__all__ = [
    'guild',
    'guild_raw'
]

from typing import Dict, Optional, Any  # 'Dict' only for backwards compatibility (for <3.9)

from Wrappers.util import api_call


def guild(name: str) -> Optional[Dict[str, Any]]:
    """
    Wrapper for "guild" requests.

    Changed from raw response:
    - 'request' object was removed (so there is only guild data)

    :param name: name of requested guild
    :return: if found: dict of guild's data; else None
    """
    data = api_call('legacy', {'action': 'guildStats', 'command': name})

    if 'error' in data:  # if not found
        return

    del data['request']  # so there is only guild data

    return data


def guild_raw(name: str) -> Dict[str, Any]:
    """
    Returns raw response.

    :param name: name of requested guild
    :return: dict obtained from response
    """
    return api_call('legacy', {'action': 'guildStats', 'command': name})
