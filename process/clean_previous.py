import time
import pandas as pd 
import numpy as np
from textdistance import levenshtein

from .lib.shared.config import *
from .lib import utils

df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/master_players.csv")
df = df[df['avg_xGBuildup'].notna()]
df = df[df['kickoff_time'] < '2023-08-10']

spi = pd.read_csv('/Users/calvinwalker/Downloads/soccer-spi/spi_matches.csv')

spi = spi[(spi['league'] == 'Barclays Premier League') | (spi['league'] == 'French Ligue 1') | (spi['league'] == 'English League Championship') |
            (spi['league'] == 'German Bundesliga') | (spi['league'] == 'Italy Serie A') | (spi['league'] == 'Spanish Primera Division')]


matches = [(name1, name2) for name1 in np.unique(spi['team1']) for name2 in np.unique(df['h_team']) 
            if levenshtein(name1[:min(len(name1), len(name2))], name2[:min(len(name1), len(name2))]) <= 1 
            and name1 != name2 and name1 != 'Brest' and name1 != 'Lecce' and name2 != 'Brest']

matches.append(("AFC Bournemouth", "Bournemouth"))
matches.append(("RB Leipzig", "RasenBallsport Leipzig"))
matches.append(("VfL Wolfsburg", "Wolfsburg"))
matches.append(("Borussia Monchengladbach", "Borussia M.Gladbach"))
matches.append(("SC Freiburg", "Freiburg"))
matches.append(("FC Augsburg", "Augsburg"))
matches.append(("Sevilla FC", "Sevilla"))
matches.append(("AS Monaco", "Monaco"))
matches.append(("St Etienne", "Saint-Etienne"))
matches.append(("1. FC Union Berlin", "Union Berlin"))
matches.append(("Spal", "SPAL 2013"))
matches.append(("AS Roma", "Roma"))
matches.append(("TSG Hoffenheim", "Hoffenheim"))
matches.append(("Athletic Bilbao", "Athletic Club"))

for name1, name2 in matches:
    spi.loc[spi['team1'] == name1, 'team1'] = name2
    spi.loc[spi['team2'] == name1, 'team2'] = name2

# print(np.unique(spi['team1']))
# print(np.unique(df['h_team']))

spi.drop(columns=['prob1','prob2','probtie', 'proj_score1', 'proj_score2', 'importance1', 'importance2', 'score1','score2', 'xg1', 'xg2', 'nsxg1', 'nsxg2', 'adj_score1', 'adj_score2'], inplace=True)

for i, row in df.iterrows():

    print(i)

    date, t1, t2 = row['kickoff_time'], row['h_team'], row['a_team']

    if date == "2023-04-30" and t1 == "Strasbourg" and t2  == "Lyon":
        continue

    print(date, t1, t2)

    if date > '2023-08-10':
        continue

    # print(spi['date'])
    # print(spi.loc[(spi['date'] == date) & (spi['team1'] == t1) & (spi['team2'] == t2), 'spi1'])
    # print(spi[spi['date'] == date])

    df.loc[i, 'spi1'] = spi.loc[(spi['date'] == date) & (spi['team1'] == t1) & (spi['team2'] == t2), 'spi1'].values[0]
    df.loc[i, 'spi2'] = spi.loc[(spi['date'] == date) & (spi['team1'] == t1) & (spi['team2'] == t2), 'spi2'].values[0]

# df = df.merge(spi, left_on=['kickoff_time', 'h_team', 'a_team'], right_on=['date', 'team1', 'team2'])

print(df.loc[:, ['was_home', 'spi1', 'spi2']])

# for col in df.columns:
#     print(col)

df.loc[df['was_home'] == True, 'team_spi'] = df.loc[df['was_home'] == True, 'spi1']
df.loc[df['was_home'] == True, 'opponent_spi'] = df.loc[df['was_home'] == True, 'spi2']
df.loc[df['was_home'] == False, 'team_spi'] = df.loc[df['was_home'] == False, 'spi2']

df.loc[df['was_home'] == False, 'opponent_spi'] = df.loc[df['was_home'] == False, 'spi1']

print(df.loc[:, ['team_spi', 'was_home', 'opponent_spi', 'spi1', 'spi2']])


df.to_csv('/Users/calvinwalker/Documents/Projects/FPL/data/training_data.csv')