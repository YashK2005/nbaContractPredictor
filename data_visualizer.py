from matplotlib import pyplot as plt
import numpy as np
from database_setup import data_plot_fetcher

indexes = {
    "player_id" : 0,
    #"first_name" : 1,
    #"last_name" : 2,
    "height" : 3,
    "weight" : 4,
    "experience" : 5,
    #"birth_date" : 6,
    "salary" : 7,
    #"player_id:1" : 8,
    "games_played" : 9,
    "minutes" : 10,
    "fg" : 11,
    "fga" : 12,
    "three_pt" : 13,
    "three_pta" : 14,
    "ft" : 15,
    "fta" : 16,
    "pts" : 17,
    "reb" : 18,
    "ass" : 19,
    "stl" : 20,
    "blk" : 21,
    "turn" : 22,
    "pf" : 23,
    "tspct" : 24,
    "usg" : 25,
    "per" : 26,
}

def find_ideal_parameters():
    #selecting best parameters for model by calculating pearson coefficients for 40+ stats
    independent = "three_pt"
    x = np.array([])
    salary = np.array([])
    data = (data_plot_fetcher())
    for sample in data:
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
            x = np.append(x, [sample[indexes[independent]]])
            salary = np.append(salary, [sample[indexes["salary"]]])
    #print(x, salary)
    a, b = np.polyfit(x, salary, 1)

    print(np.corrcoef(x, salary))
    plt.scatter(x, salary)
    plt.plot(x, a*x + b)
    plt.xlim(left=0)
    plt.ylim(bottom=0)

    plt.xlabel(independent)
    plt.ylabel("salary")
    plt.show()


    #calculating pearson coefficients for each player to select best variables

    #getting games_played and salary arrays as these will be used many times
    salary = np.array([])
    games_played = np.array([])
    for sample in data:
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                games_played = np.append(games_played, [sample[indexes["games_played"]]])
                salary = np.append(salary, [sample[indexes["salary"]]])
    salary = np.sqrt(salary)
    #calcuating pearson coefficient for each total 
    for key in indexes: 
        x = np.array([])
        for sample in data:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                x = np.append(x, [sample[indexes[key]]])
        print(key)
        print(np.corrcoef(x, salary))

    #calculating pearson coefficinet on per game stats
    for key in indexes:
        x = np.array([])
        for sample in data:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                x = np.append(x, [sample[indexes[key]]])
        
        x_per_gp = np.divide(x, games_played)
        print(key, "/gp")
        print(np.corrcoef(x_per_gp, salary))
                
    #calculating pearson coefficient on fg%, 3pt%, ft%

    fg_pct = np.array([])
    three_pt_pct = np.array([])
    ft_pct = np.array([])

    for sample in data:
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
            fg = sample[indexes["fg"]]
            fga = sample[indexes["fga"]]
            result = fga and fg / fga or 0  # fg / fga (returns 0 when dividing by 0)
            fg_pct = np.append(fg_pct, [result])
            
            three_pt = sample[indexes["three_pt"]]
            three_pta = sample[indexes["three_pta"]]
            result = three_pta and three_pt / three_pta or 0
            three_pt_pct = np.append(three_pt_pct, [result])

            ft = sample[indexes["ft"]]
            fta = sample[indexes["fta"]]
            result = fta and ft / fta or 0
            ft_pct = np.append(ft_pct, [result])


    print("fg%")
    print(np.corrcoef(fg_pct, salary))
    print("three_pt%")
    print(np.corrcoef(three_pt_pct, salary))
    print("ft%")
    print(np.corrcoef(ft_pct, salary))

def gradient_descent_input_fetcher():
    #order of outputs:
    '''
    0: Exp 0.43
    1: Minutes 0.55
    2: Fg 0.72
    3: Fga 0.69
    4: Threept 0.44
    5: Threepta 0.45
    6: Ft 0.70
    7: Fta 0.69 
    8: Pts 0.73
    9: Reb 0.43
    10: Ass 0.59
    11: Stl 0.44
    12: Turn 0.65
    13: Usg 0.65
    14: Per 0.65
    15: minutes/gp 0.70
    16: fg/gp 0.80
    17: fga/gp 0.76
    18: three_pt/gp 0.47
    19: threepta/gp 0.47
    20: ft/gp 0.75
    21: fta/gp 0.73
    22: Pts /gp 0.80
    23: reb/gp 0.48
    24: ass/gp 0.62
    25: Stl / gp 0.48
    26: Turn/gp 0.71
    27: pf/gp 0.42
    '''

    #fetch total stats (0-14)
    raw_data = data_plot_fetcher()
    result_data = []
    keys = ["experience", "minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "usg", "per"]
    for sample in raw_data:
        key_data = []
        keys = ["experience", "minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "usg", "per"]
        for key in keys:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                key_data.append(sample[indexes[key]])
        keys = ["minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "pf"]
        for key in keys:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                key_data.append(sample[indexes[key]] / sample[indexes["games_played"]])
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
            result_data.append(key_data) 

    result_data = np.array(result_data)
    return result_data

def new_gradient_descent_input_fetcher(): #testing gradient_descent with different parameters
    #order of outputs:
    '''
    0: Usg
    1: Per
    2: Total Minutes
    3: Minutes/gp
    4: Fg/gp
    5: Fga/gp
    6: Three_pt/gp
    7: Three_pta/gp
    8: Pts/gp
    9: Reb/gp
    10: Ass/gp
    11: Stl/gp
    12: Blk/gp
    13: Turn/gp
    14: Pf/gp
    '''
    raw_data = data_plot_fetcher()
    result_data = []
    for sample in raw_data:
        key_data = []
        keys = ['usg', 'per', 'minutes']
        for key in keys:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                key_data.append(sample[indexes[key]])
        keys = ["minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "blk", "turn", "pf"]
        for key in keys:
            if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
                key_data.append(sample[indexes[key]] / sample[indexes["games_played"]])
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
            result_data.append(key_data) 
    result_data = np.array(result_data)
   
    #print(np.shape(result_data))
    return result_data
        

def gradient_descent_output_fetcher():
    raw_data = data_plot_fetcher()
    salaries = []
    for sample in raw_data:
        if sample[indexes["salary"]] > 1000000 and sample[indexes["games_played"]] > 0:
            salaries.append(sample[indexes["salary"]])
    salaries = np.array(salaries)
    return salaries

def individual_input_output(data): #gets input, output, for a single player
    keys = ["experience", "minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "usg", "per"]
    input_data = []
    keys = ["experience", "minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "usg", "per"]
    for key in keys:
        if data[indexes["salary"]] > 1000000 and data[indexes["games_played"]] > 0:
            input_data.append(data[indexes[key]])
    keys = ["minutes", "fg", "fga", "three_pt", "three_pta", "ft", "fta", "pts", "reb", "ass", "stl", "turn", "pf"]
    for key in keys:
        if data[indexes["salary"]] > 1000000 and data[indexes["games_played"]] > 0:
            input_data.append(data[indexes[key]] / data[indexes["games_played"]])
    if data[indexes["salary"]] > 1000000 and data[indexes["games_played"]] > 0:
            output = (data[indexes["salary"]])
    return input_data, output
    










