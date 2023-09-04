import pandas as pd 
import numpy as np

from .config import *

#TODO: weighted average? 

def average(df, season, start_week, player_name: str, stat: str) -> float: 
        """
        Averages the given players stats over the past n weeks 
        """

        index = SEASONS.index(season)
        weeks= PAST_WEEKS_TO_AVERAGE 

        val = 0
        dnom = 0

        for gameweek in range(start_week - 1, start_week - weeks - 1, -1):

            if gameweek <= 0:
                 gameweek = 38 + gameweek
                 season = SEASONS[index - 1]
                 index -= 1

            try:
                val += df.loc[(df["GW"] == gameweek) 
                            & (df["name"] == player_name), 
                            stat].values[0]

                dnom += 1

            except IndexError:
                continue
        
        if dnom == 0:
            return 0

        return val / dnom

def moving_average(df, season, gameweek, player_name: str, stat: str) -> float:

    last = df.loc[(df['season'] == season) &
                  (df["GW"] == gameweek) &
                  (df["name"] == player_name), stat].values[0]
       
    if gameweek == 1:
        gameweek = 39
        season = SEASONS[SEASONS.index(season) - 1]


    moving = df.loc[(df['season'] == season) &
                    (df["GW"] == (gameweek - 1)) &
                    (df["name"] == player_name), (f'average_{stat}')].values[0]

    return (last + moving) / PAST_WEEKS_TO_AVERAGE
