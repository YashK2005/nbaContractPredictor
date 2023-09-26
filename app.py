from flask import Flask, render_template, request
from predicting_salary import predictor
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_salary = None
    actual_salary = None
    message = None
    player_not_found = False

    if request.method == 'POST':
        first_name = (request.form['first_name'].strip()).capitalize()
        last_name = (request.form['last_name'].strip()).capitalize()
        full_name = first_name + " " + last_name
        predicted_salary, actual_salary = predictor(first_name, last_name)
        predicted_salary = int(predicted_salary)
        
        print(predicted_salary, actual_salary)

        if predicted_salary > actual_salary:
            diff = f"{(predicted_salary - actual_salary):,}"
            message = full_name + " is underpaid by $" + diff + "."
        elif predicted_salary < actual_salary:
            diff = f"{(actual_salary - predicted_salary):,}"
            message = full_name + " is overpaid by $" + diff + "."
        else:
            message = full_name + " is paid fairly."
        if predicted_salary == 0: 
            message = "Player not found. Check spelling and try again."
            player_not_found = True
        
        predicted_salary = f"{predicted_salary:,}"
        actual_salary = f"{actual_salary:,}"
    return render_template('index.html', predicted_salary=predicted_salary, actual_salary=actual_salary, message=message, player_not_found=player_not_found)

@app.route('/how_does_this_work')
def how_does_this_work():
    return render_template('how_does_this_work.html')

if __name__ == '__main__':
    app.run(debug=True)

