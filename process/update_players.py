import pandas as pd
import requests
import os

def get_and_write_most_recent():

    path = "/Users/calvinwalker/Documents/Projects/FPL/data/2023-24/players"

    for file in os.listdir(path):

        filename = os.fsdecode(file)
        id = filename.split('_')[-1]
        df = pd.read_csv(f"{path}/{file}/gw.csv")

        most_recent_fixture = requests.get(
            f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        ).json()["history"][-1]

        game_result = pd.DataFrame(most_recent_fixture, index=[0])

        df = pd.concat([df, game_result], ignore_index=True)  
        df.to_csv(f"{path}/{file}/gw.csv")

get_and_write_most_recent()