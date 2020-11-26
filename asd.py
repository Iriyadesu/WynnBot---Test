import requests
from datetime import date

r = requests.get(f'https://api.wynncraft.com/public_api.php?action=guildStats&command=bovemianRhapsody')
    #get the data
json = r.json()

niggalist = []

def diff_dates(date1, date2):
    return abs(date2-date1).days


for nigger in json['members']:
    r2 = requests.get(f'https://api.wynncraft.com/v2/player/' +nigger['name'] + "/stats")
    json2 = r2.json()
    d2 = date(2020,11,15)
    d1 = json2['data'][0]['meta']['lastJoin'][:10].split('-')
    d3 = ",".join(d1)
    result1 = diff_dates(d2, date(int(d1[0]),int(d1[1]),int(d1[2])))
    print("Name: " + json2['data'][0]['username'] + " Last joined: " + str(result1))





