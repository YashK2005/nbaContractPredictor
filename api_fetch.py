import requests
import json

KEY = 'c08e20fc0f3b4261b2f53a59b981415b'
SALARY_URL = 'https://api.sportsdata.io/v3/nba/scores/json/Players?key=' + KEY
STATS_URL = 'https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStats/2023?key=' + KEY

def getSalary(): #getting relevant data from STATS_URL link
    salary_json = requests.get(SALARY_URL).json()
    count = 0
    data = []
    for player in salary_json:
        id = player['PlayerID']
        first_name = player["FirstName"]
        last_name = player["LastName"]
        height = player["Height"]
        weight = player["Weight"]
        experience = player["Experience"]
        birth_date = player["BirthDate"]
        salary = player["Salary"]

        if (id != None and first_name!= None and last_name != None and height != None and weight != None and experience != None and birth_date!= None and salary != None):
            if int(experience) >= 1:
                #print(id, first_name, last_name, height, weight, experience, birth_date, salary)
                count += 1
                data.append([id, first_name, last_name, height, weight, experience, birth_date, salary])
    #print(count)
    return data

def getStats(): #getting relevant data from SALARY_URL link
    stats_json = requests.get(STATS_URL).json()
    count = 0
    data = []
    for player in stats_json:
        id = player['PlayerID']
        name = player['Name']
        games_played = player['Games']
        minutes = player['Minutes']
        fg = player['FieldGoalsMade']
        fga = player['FieldGoalsAttempted']
        three_pt = player['ThreePointersMade']
        three_pta = player['ThreePointersAttempted']
        ft = player['FreeThrowsMade']
        fta = player['FreeThrowsAttempted']
        pts = player['Points']
        reb = player['Rebounds']
        ass = player['Assists']
        stl = player['Steals']
        blk = player['BlockedShots']
        turnovers = player['Turnovers']
        pf = player['PersonalFouls']
        tspct = player['TrueShootingPercentage']
        usg = player['UsageRatePercentage']

        if (id != None and name!= None and games_played != None and minutes != None and fg != None and fga != None and three_pt != None and three_pta != None and ft != None and fta != None and pts != None and reb != None and ass != None and stl != None and blk != None and turnovers != None and pf != None and tspct != None and usg != None):
            #print(id, name, games_played, minutes, fg, fga, three_pt, three_pta, ft, fta, pts, reb, ass, stl, blk, turnovers, pf, tspct, usg)
            count += 1
            data.append([id, games_played, minutes, fg, fga, three_pt, three_pta, ft, fta, pts, reb, ass, stl, blk, turnovers, pf, tspct, usg])
    #print(count)
    return data


def get_per(): #Gettign Player Efficiency Rating (PER) from STATS_URL link
    stats_json = requests.get(STATS_URL).json()
    count = 0
    data = []
    for player in stats_json:
        id = player['PlayerID']
        per = player['PlayerEfficiencyRating']
        data.append([per, id])
    return data