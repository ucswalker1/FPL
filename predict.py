import glob
import joblib
import requests

import pandas as pd
from process.lib.config import *

def load_fix():

    df = pd.DataFrame()

    info = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    n = len(info['elements'])

    # for i in range(n):
    for i in range(n):

        first = info['elements'][i]['first_name']
        last = info['elements'][i]['second_name']

        player_df = pd.DataFrame()

        first = info['elements'][i]['first_name']
        last = info['elements'][i]['second_name']
        
        price = str(info['elements'][i]['now_cost'])

        if len(price) == 3:
            price = float(f'{price[:2]}.{price[2:]}')
        else:
            price = float(f'{price[0]}.{price[1]}')


        team = info['elements'][i]['team']
        ownership = info['elements'][i]['selected_by_percent']

        name = first + ' ' + last
        id = info['elements'][i]['id']
        pos = info['elements'][i]['element_type']

        elem = requests.get(
            f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        ).json()

        data = elem['fixtures'][0]
        is_home = data['is_home']

        team_h = TEAMS[data['team_h'] - 1]
        team_a = TEAMS[data['team_a'] - 1]

        if is_home:
            team_spi = SPI[team_h]
            opponent_spi = SPI[team_a]
        else:
            team_spi = SPI[team_a]
            opponent_spi = SPI[team_h]

        player_df = pd.DataFrame(
            data = [[is_home, name, id, team_spi, opponent_spi, pos, price, team, ownership]],
            columns = ['was_home', 'name', 'id', 'team_spi', 'opponent_spi', 'position', 'price', 'team', 'ownership']
        )

        #search for player 
        if not glob.glob(f'/Users/calvinwalker/Documents/Projects/FPL/data/clean/{first}_{last}*'):
            continue

        path = glob.glob(f'/Users/calvinwalker/Documents/Projects/FPL/data/clean/{first}_{last}*')[0]

        stats = pd.read_csv(path)
        stats.drop(columns=['was_home'], inplace=True)

        player_df = pd.merge(player_df, stats.tail(1), on=["name"], suffixes=['', '_y'])
        player_df.drop(player_df.filter(regex='_y$').columns, axis = 1, inplace=True)

        df = pd.concat([df, player_df], ignore_index=True)

    return df

if __name__ == "__main__":

    data = load_fix()
    print(data)

    fwd = data[data['position'] == 4]
    mid = data[data['position'] == 3]
    def_ = data[data['position'] == 2]
    gk = data[data['position'] == 1]

    print("---- collected data ----")

    #load model 

    predicitons = pd.DataFrame()

    i = 4
    for pos, features in [
            (fwd, FWD_FEATURES),
            (mid, MID_FEATURES), 
            (def_, DEF_FEATURES),
            (gk, GK_FEATURES),
    ]: 
        
        filter = ['name'] + features

        pos_df = pos.loc[:, filter]
        pos_df.dropna(inplace=True)


        print(f"---- loading model {i} ----")

        model = joblib.load(
            f"/Users/calvinwalker/Documents/Projects/FPL/models/model_{i}.pkl"
        )

        x = pos_df.loc[:, features]

        pos['xPoints'] = model.predict(x)
        pos = pos.loc[:, ['name', 'team', 'position', 'price', 'ownership', 'xPoints']]

        pos.to_csv(f'/Users/calvinwalker/Documents/Projects/FPL/pred_{i}.csv')

        pos['team'] = pos['team'].map(lambda x: TEAMS[x - 1])

        if i == 4:
            pos['position'] = 'FWD'
        elif i == 3:
            pos['position'] = 'MID'
        elif i == 2:
            pos['position'] = 'DEF'
        else:
            pos['position'] = 'GK'

        predicitons = pd.concat([predicitons, pos], ignore_index=True)
        i -= 1
    
    predicitons.to_json('/Users/calvinwalker/Documents/Projects/FPL/predictions.json', orient="records")

    #return json of predictions
    #Name, Team, Positon, FPL Price, ownership %, xPoints

