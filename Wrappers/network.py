
from Wrappers.__init__ import api_call


def player_sum() -> int:
    return api_call('https://api.wynncraft.com/public_api.php?action=onlinePlayersSum')['players_online']


def players_on_worlds() -> dict:
    data = api_call('https://api.wynncraft.com/public_api.php?action=onlinePlayers')
    del data['request']

    return data
