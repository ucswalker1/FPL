import os
import time
import glob 

import pandas as pd 
import numpy as np

from lib.config import *

pd.options.mode.chained_assignment = None 
master = pd.DataFrame()

path = '/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/players'

ids_df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/uuids.csv", usecols=['id', 'u_id'])
ids_df = ids_df.dropna()

fpl_id_to_uid = {int(fpl_id): int(u_id) for fpl_id, u_id in zip(ids_df['id'], ids_df['u_id'])}

for file in os.listdir(path):

    filename = os.fsdecode(file)
    try:
        first, last, fpl_id = filename.split('_')
    except ValueError:
        print(filename)

    understat_id = fpl_id_to_uid.get(int(fpl_id), False)

    if not understat_id:
        continue

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

    stat_search = f'/Users/calvinwalker/Documents/Projects/FPL/data/understat/*{understat_id}.csv' 

    # fix this!!
    if not glob.glob(stat_search):
        print(stat_search, first, last, fpl_id, understat_id)
        continue
        # raise ValueError
    
    for f in glob.glob(stat_search):

        # print(f)

        df_stats = pd.read_csv(f)
        df_stats.drop(columns=['season'])

        df_stats.rename(columns={'date': 'kickoff_time'}, inplace=True)
        df_player = pd.merge(df, df_stats, on='kickoff_time', suffixes=('', '_y'))
        df_player.drop(df_player.filter(regex='_y$').columns, axis = 1, inplace=True)

    df = df_player

    df['name'] = name
    df['id'] = id

    df = df.sort_values(by=['kickoff_time'], ascending=True, ignore_index=True)
    # print(df['kickoff_time'].head(10))
    length = df.shape[0] - 1
    # width = df.shape[1] - 1

    for j, row in df.iterrows():

        if j >= PAST_WEEKS_TO_AVERAGE: 

            # print(f"averaging: {row['kickoff_time']} ")

            for stat in STATS_TO_AVERAGE: 

                num = 0 

                for i in range(1, PAST_WEEKS_TO_AVERAGE + 1):

                    num += df.iloc[j - i].loc[stat]

                df.loc[j, f'avg_{stat}'] = num / PAST_WEEKS_TO_AVERAGE
                # df.iloc[row[0], width + j] = num // PAST_WEEKS_TO_AVERAGE

    df = df.iloc[10:]
    df.dropna(axis=1, inplace=True)
    df.to_csv(f'/Users/calvinwalker/Documents/Projects/FPL/data/clean/{first}_{last}.csv')
    master = pd.concat([master, df])

master.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/players_clean_all.csv')

