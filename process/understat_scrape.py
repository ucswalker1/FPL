import pandas as pd
import requests
import json
import glob
import time
from bs4 import BeautifulSoup

START_OF_SEASON = '2023-08-10'


def update_existing():

    data = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/understat/understat_player.csv')

    ids = data['id']
    names = data['player_name']

    for id, name in list(zip(ids, names)):

        start_time = time.time()

        url = f'https://understat.com/player/{id}'
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'lxml')

        t = soup.find_all('div', {'class': 'block'})[-1].find('script')
        
        string = t.string
        idx_start = string.index("('") + 2
        idx_end = string.index("')")

        json_data = string[idx_start:idx_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')

        new_data = json.loads(json_data)

        if len(name.split()) == 1:
            first, last = name, ''
        else:
            first, last = name.split(maxsplit=1)

        stat_search = f'/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/understat/{first}_{last}_*'

        for f in glob.glob(stat_search):
            df = pd.read_csv(f)

        for game in new_data:
            date = game['date']

            if date < START_OF_SEASON:
                break

            elif date in df['date'].values:
                continue
            
            to_add = pd.DataFrame.from_records([game])
            df = pd.concat([to_add, df], ignore_index=True)

        df.to_csv(f'/Users/calvinwalker/Documents/Projects/FPL/data/understat/{first}_{last}_{id}.csv')

        print(f"--- updated {name} in {time.time() - start_time} seconds ---")

def create_new():

    ids_df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/uuids.csv", usecols=['u_id'])
    ids_df = ids_df.dropna()

    data = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/understat/understat_player.csv')
    seen_ids = data['id']
    
    i = 0
    for id in ids_df['u_id']:
        
        if id in seen_ids.values:
            continue
        
        url = f'https://understat.com/player/{int(id)}'
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'lxml')

        t = soup.find_all('div', {'class': 'block'})[-1].find('script')
        
        string = t.string
        idx_start = string.index("('") + 2
        idx_end = string.index("')")

        json_data = string[idx_start:idx_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')

        new_data = json.loads(json_data)

        df = pd.DataFrame()

        for game in new_data:
            date = game['date']
            
            to_add = pd.DataFrame.from_records([game])
            df = pd.concat([to_add, df], ignore_index=True)

        # print(df)
        # print([col for col in df.columns])
        df.to_csv(f'/Users/calvinwalker/Documents/Projects/FPL/data/understat/_{int(id)}.csv')

create_new()