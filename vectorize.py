import pandas as pd
from lib.config import * 

df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")

df['position'] = [POSITION_TO_INT[pos] for pos in df['position']]
df['team'] = [TEAM_TO_INT[team] for team in df['team']]

df.to_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")