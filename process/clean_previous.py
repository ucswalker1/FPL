import time
import pandas as pd 
import numpy as np

from .lib.config import *

def clean():

    def average(from_gw, prev_weeks, player, stat) -> float: 
        """
        Average stat for the given player starting with from_gw over
        the previous prev_weeks
        """

        val = 0
        denom = 0

        for i in range(from_gw - 1, from_gw - prev_weeks - 1, -1):

            try:
                val += df.loc[(df["GW"] == i) 
                            & (df["name"] == player), 
                            stat].values[0]
                
                denom += 1

            except IndexError:
                continue
        
        if denom == 0:
            return 0

        return val / denom

    df = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/gws/merged_gw.csv')

    for week in range(PAST_WEEKS_TO_AVERAGE + 1, 39):

        start_time = time.time()

        print(week)

        for player in np.unique(df[df["GW"] == week]["name"]):
            for stat in STATS_TO_AVERAGE:

                df.loc[(df["GW"] == week) & (df["name"] == player),
                    (f"average_{stat}")] = average(
                        week, PAST_WEEKS_TO_AVERAGE, player, stat
                        )

        print(df[df["GW"] == week])
        print(f"----- {time.time() - start_time} seconds ------ for week {week}")

    df['position'] = [POSITION_TO_INT[pos] for pos in df['position']]
    df['team'] = [TEAM_TO_INT[team] for team in df['team']]

    df.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages.csv')
                
if __name__ == "__main__":
    clean() 




# for i in range(PAST_WEEKS_TO_AVERAGE, len(SEASONS) * 38):

#     week = i % 38
#     season = SEASONS[i // 38]

#     df = df.loc[df['season_x'] == season]


