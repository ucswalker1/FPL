import pandas as pd

from lib.config import * 

df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")

df['position'] = [POSITION[pos] for pos in df['position']]
df['team'] = [team_to_int[team] for team in df['team']]

df.to_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")