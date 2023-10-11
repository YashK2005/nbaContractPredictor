# [NBA Contract Predictor](http://nbacontractpredictor.pythonanywhere.com)
#### [Click for link to website](http://nbacontractpredictor.pythonanywhere.com)

Using machine learning algorithms to analyze NBA players contracts and determine whether players are underpaid or overpaid.

This project uses supervised machine learning (linear regression) to predict a NBA player's salary based on their stats, and then compares their expected salary to their actual salary to determine if the player is underpaid or overpaid. The first step was collecting data about NBA players and their stats and salaries. I used the SportsData.io API to fetch jsons containing the stats and salaries of over 340 players. I then parsed and organized the raw data into SQLite database tables.

Next, I used the matplotlib and numpy libraries to create scatter plots for stats vs salary. I also calculated the pearson correlation coefficient between stats and salary to determine which statistics had a highest impact on a player's salary. I tested over 50 stats, and ultimately picked 28 parameters for my model.

Once I decided on the parameters, I created functions to fetch the relevant statsitics from the database. For the machine learning algorithm, I first used z-score normalization on my features, to ensure that all features had a similar range of values (originally some features had a range 100 times greater than other features).

I then created a mean squared error function to compute the cost. I used numpy arrays instead of python's built-in arrays to improve the speed of the algorithm, since numpy uses vectorized operations. I then computed the partial derivative of the cost function to come up formulas for gradient descent.

After testing learning rates, I ran the gradient descent alogrithm for 100,000 iterations, and recorded the weights for each parameter. Finally, I created a prediction function, which fetches a player's stats from the database, normalizes the stats, and then computes the player's expected salary. I compare it with the player's actual salary to determine if the player is overpaid or underpaid.

Finally, I created a [web app](http://nbacontractpredictor.pythonanywhere.com) using Flask, Python, HTML, and CSS.
