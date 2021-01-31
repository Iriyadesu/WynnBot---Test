
from Wrappers.__init__ import api_call


def player_sum() -> int:
    return api_call('legacy', {'action': 'onlinePlayersSum'})['players_online']


def players_on_worlds() -> dict:
    data = api_call('legacy', {'action': 'onlinePlayers'})
    del data['request']

    return data
