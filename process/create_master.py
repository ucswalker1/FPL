import os
import time
import glob 

import pandas as pd 
import numpy as np

from lib.config import *

pd.options.mode.chained_assignment = None 
master = pd.DataFrame()

path = '/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/players'

for file in os.listdir(path):

    filename = os.fsdecode(file)
    first, last, id = filename.split('_')

    start_time = time.time()

    name = first + ' ' + last 

    df = pd.read_csv(f"{path}/{file}/gw.csv")
    df['GW'] = df.index + 1
    df['season'] = '2023-24'

    for season in SEASONS[-2::-1]:

        search = f'/Users/calvinwalker/Documents/Projects/FPL/data/{season}/players/{first}_{last}_*'

        for file in glob.glob(search):

            df_season = pd.read_csv(f"{file}/gw.csv")
            df_season['GW'] = df_season.index + 1
            df_season['season'] = season
            
            df = pd.concat([df, df_season], ignore_index=True)      

    df['kickoff_time'] = [date[:10] for date in df['kickoff_time']]   

    stat_search = f'/Users/calvinwalker/Documents/Projects/FPL/data/understat/{first}_{last}_*' 

    for f in glob.glob(stat_search):

        df_stats = pd.read_csv(f)
        df_stats.drop(columns=['season'])

        df_stats.rename(columns={'date': 'kickoff_time'}, inplace=True)
        df_player = pd.merge(df, df_stats, on='kickoff_time', suffixes=('', '_y'))
        df_player.drop(df_player.filter(regex='_y$').columns, axis = 1, inplace=True)
    
    df = df_player

    df['name'] = name
    df['id'] = id

    df = df[::-1]
    length = df.shape[0] - 1
    # width = df.shape[1] - 1

    for row in df.itertuples():

        if length - row[0] >= PAST_WEEKS_TO_AVERAGE: 

            for stat in STATS_TO_AVERAGE: 

                num = 0 

                for i in range(1, PAST_WEEKS_TO_AVERAGE + 1):

                    num += df.iloc[row[0] + i].loc[stat]

                df.loc[row[0], f'avg_{stat}'] = num / PAST_WEEKS_TO_AVERAGE
                # df.iloc[row[0], width + j] = num // PAST_WEEKS_TO_AVERAGE

    # print(df['season'].value_counts())
    # break
    # print((df['avg_xGChain']).max)
    # print(df)
    # break
    print(f"cleaned {name} in {time.time() - start_time}")
    master = pd.concat([master, df])

master.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/master_players.csv')

