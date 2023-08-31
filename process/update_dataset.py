import requests
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup

import time

from lib.config import *
from lib import utils

def add_ids(df): 

    info = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    n = len(info['elements'])

    for i in range(n):
        name = info['elements'][i]['first_name'] + ' ' + info['elements'][i]['second_name']
        id = info['elements'][i]['id']
        df.loc[df['name'] == name, 'id'] = id
    
    def toint(x):
        if pd.isna(x):
            return -1 
        return int(x)
    
    df['id'] = df['id'].apply(toint)

    return df

def get_stats(gameweek, players):

    gw = requests.get(f"https://fantasy.premierleague.com/api/event/{gameweek}/live/").json()


    for player in players: 
        pass
        
    pass

if __name__ == "__main__":

    # info = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    # n = len(info['elements'])

    # df = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/master_players.csv')

    # for i in range(n):
    #     name = info['elements'][i]['first_name'] + ' ' + info['elements'][i]['second_name']
    #     id = info['elements'][i]['id']
    #     position = info['elements'][i]['element_type']

    #     df.loc[df['name'] == name, 'pos'] = position


    #     # print(df.loc[df['name'] == name, ['name', 'pos', 'was_sub']])

    # df['was_sub'] = df['position'] == 'Sub'

    # df.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/master_players.csv')

    #     # df.loc[df['name'] == name, 'id'] = id

    

    # print(df.loc[:,['date', 'team1', 'team2']])
