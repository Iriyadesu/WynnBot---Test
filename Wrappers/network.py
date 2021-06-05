"""
Wrappers for Wynncraft "network" API
"""
__all__ = [
    'player_sum',
    'players_on_worlds'
]

from Wrappers.util import api_call


def player_sum() -> int:
    return api_call('legacy', {'action': 'onlinePlayersSum'})['players_online']


def players_on_worlds() -> dict:
    data = api_call('legacy', {'action': 'onlinePlayers'})
    del data['request']

    return data
