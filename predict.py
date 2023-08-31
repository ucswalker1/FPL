import joblib
import requests

import pandas as pd
from process.lib.config import *

def load_fixtures(week="Gameweek 4"):

    df = pd.DataFrame()

    info = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    n = len(info['elements'])

    names = []
    ids = []
    pos = []

    for i in range(n):

        # print(info['elements'][i].keys())
        
        names.append(
            info['elements'][i]['first_name'] + 
            ' ' + info['elements'][i]['second_name']
        )

        ids.append(info['elements'][i]['id'])
        pos.append(info['elements'][i]['element_type'])


    is_home = []
    team_spi = []
    opponent_spi = []

    for id in ids: 

        elem = requests.get(
            f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        ).json()

        data = elem['fixtures'][0]
        is_home.append(data['is_home'])

        team_h = TEAMS[data['team_h'] - 1]
        team_a = TEAMS[data['team_a'] - 1]
        team_spi.append(SPI[team_h])
        opponent_spi.append(SPI[team_a])

    #prices
    df['was_home'] = is_home
    df['name'] = names
    df['id'] = ids
    df['team_spi'] = team_spi
    df['opponent_spi'] = opponent_spi
    
    return df

if __name__ == "__main__":

    df = load_fixtures()
    print(df)

    df1 = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/master_players.csv')

    df1['name_x'] = df1['name']
    df1 = df1.groupby('name').last()

    data = df.merge(df1, left_on=['name'], right_on=['name_x'], suffixes=['', '_y'])
    data.drop(data.filter(regex='_y$').columns, axis = 1, inplace=True)

    for column in data.columns:
        print(column)

    data = data.loc[:, FEATURES]



    # print(data.isna().any())


    #load fixtures for upcoming gameweek
    #load spi data from spi_global_rankings

    #load most recent averages from master_players

    #combine^ 

    #select Features from position 

    #load model 

    # for i in range(1, 5): 

    #     model = joblib.load(
    #         f"/Users/calvinwalker/Documents/Projects/FPL/models/model_{i}.pkl"
    #     )

        #df['xPoints'] = model.predict..

    #return json of predictions
    #Name, Team, Positon, FPL Price, ownership %, xPoints

