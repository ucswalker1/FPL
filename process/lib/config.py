### CLEANING ###

SEASONS = [
    "2016-17",
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
]
 
UNUSED = ["xP", "element", "kickoff_time", "round", "GW"]

PAST_WEEKS_TO_AVERAGE = 10

STATS_TO_AVERAGE = [  #total_points? 
            #standard FPL
            "bonus", 
            "bps", 
            "clean_sheets", 
            "creativity", 
            "expected_goals_conceded",
            "goals_conceded",
            "minutes",
            "ict_index",
            "influence",
            "red_cards",
            "threat",
            "transfers_balance",
            "yellow_cards",

            #understat
            "goals",
            "shots",
            "xG",
            "xA",
            "assists",
            "key_passes",
            "npxG",
            "xGChain",
            "xGBuildup",
]

### MAPPINGS ### 


TEAMS = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Burnley",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Liverpool",
    "Luton Town",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sheffield United",
    "Spurs",
    "West Ham",
    "Wolves",
]

TEAM_TO_INT = {team: i for i, team in enumerate(TEAMS)}

SPI = {
  'Manchester City': 92.00,
  'Liverpool' : 83.93,
  'Arsenal' : 83.92,
  'Newcastle United' : 83.70,
  'Brighton' : 80.88,
  'Aston Villa' : 79.30,
  'Manchester United' : 79.08,
  'Brentford' : 77.14,
  'Chelsea' : 75.78,
  'Crystal Palace' : 73.46,
  'Spurs' : 72.14,
  'West Ham' : 71.12,
  'Fulham' : 68.22,
  'Burnley' : 62.90,
  'Everton' : 63.63,
  'Bournemouth' : 59.58,
  'Wolves' : 59.06,
  'Luton Town' : 55.50,
  'Sheffield United' : 56.60,
  'Nottingham Forest' : 56.13,
}

POSITION_TO_INT = {
    "GK": 1,
    "DEF": 2,
    "MID": 3,
    "FWD": 4,
}

### FEATURES ### 

#TODO: add freekick/setpeice takers

FEATURES = [
            #standard FPL
            "avg_bonus", 
            "avg_bps", 
            "avg_clean_sheets", 
            "avg_creativity", 
            # "avg_expected_goals_conceded",
            "avg_goals_conceded",
            "avg_minutes",
            "avg_ict_index",
            "avg_influence",
            "avg_red_cards",
            "avg_threat",
            "avg_transfers_balance",
            "avg_yellow_cards",
            # "team",
            # "opponent_team",
            "was_home",

            #understat
            "avg_goals",
            "avg_shots",
            "avg_xG",
            "avg_xA",
            "avg_assists",
            # "avg_key_passes",
            "avg_npxG",
            "avg_xGChain",
            "avg_xGBuildup",

            "penalties_saved", 
            "saves",
            # "average_goals_conceded",
]


FWD_FEATURES = [

        "avg_bonus", 
        "avg_bps", 
        "avg_creativity",
        "avg_minutes",
        "avg_ict_index",
        "avg_influence",
        "avg_transfers_balance",
        # "avg_yellow_cards",
        "team_spi",
        "opponent_spi",
        "was_home",

        #understat
        "avg_goals",
        "avg_shots",
        "avg_xG",
        "avg_xA",
        "avg_assists",
        # "avg_key_passes",
        "avg_npxG",
        "avg_xGChain",
        "avg_xGBuildup",
]
    
MID_FEATURES = [

    "avg_clean_sheets", 
    "avg_goals_conceded",

    "avg_bonus", 
    "avg_bps", 
    "avg_creativity",
    "avg_minutes",
    "avg_ict_index",
    "avg_influence",
    "avg_transfers_balance",
    # "avg_yellow_cards",
    "team_spi",
    "opponent_spi",
    "was_home",


    #understat
    "avg_goals",
    "avg_shots",
    "avg_xG",
    "avg_xA",
    "avg_assists",
    # "avg_key_passes",
    "avg_npxG",
    "avg_xGChain",
    "avg_xGBuildup",

]

DEF_FEATURES = [

    "avg_clean_sheets", 
    "avg_goals_conceded",

    "avg_bonus", 
    "avg_bps", 
    "avg_creativity",
    "avg_minutes",
    "avg_ict_index",
    "avg_influence",
    "avg_transfers_balance",
    # "avg_yellow_cards",
    "team_spi",
    "opponent_spi",
    "was_home",

    #understat
    "avg_goals",
    "avg_shots",
    "avg_xG",
    "avg_xA",
    "avg_assists",
    # "avg_key_passes",
    "avg_npxG",
    "avg_xGChain", #often the same?? 
    "avg_xGBuildup",#often the same?? 
]

#seperate specification
GK_FEATURES = [
    "penalties_saved", 
    "saves",
    "avg_clean_sheets", 
    "avg_transfers_balance",
    # "avg_goals_conceded",
    "team_spi",
    "opponent_spi",
    "was_home",
]

FEATURE_MAP = {
    4 : FWD_FEATURES,
    3 : MID_FEATURES,
    2 : DEF_FEATURES, 
    1 : GK_FEATURES,
}

# fixture,goals_conceded,goals_scored,ict_index,influence,kickoff_time,minutes,
# opponent_team, own_goals,penalties_missed,penalties_saved,red_cards,round,
# saves,selected,starts,team_a_score, team_h_score,threat,total_points,
# transfers_balance,transfers_in,transfers_out,value,was_home, yellow_cards,GW