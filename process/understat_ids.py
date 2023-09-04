import pandas as pd
import requests
import json
import glob
import time
from bs4 import BeautifulSoup


url = 'https://understat.com/league/EPL'
r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

t = soup.find_all('div', {'class': 'block'})[-1].find('script')

string = t.string
idx_start = string.index("('") + 2
idx_end = string.index("')")

json_data = string[idx_start:idx_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

data = json.loads(json_data)

d = {}
for i, player in enumerate(data):
    d[i] = [player['player_name'], player['id']]

df = pd.DataFrame.from_dict(d, orient='index', columns=['u_name', 'u_id'])
fpl = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/player_idlist.csv', dtype={'id': int})

fpl['fpl_name'] = fpl['first_name'] + ' ' + fpl['second_name']

print(fpl.dtypes)
fpl = fpl.merge(df, left_on=['fpl_name'], right_on=['u_name'], how='outer')
print(fpl.dtypes)
fpl.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/uuids.csv')
