from matplotlib import pyplot as plt
import numpy as np
from database_setup import data_plot_fetcher

#selecting best parameters for model

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








