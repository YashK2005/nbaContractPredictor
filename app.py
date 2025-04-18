from flask import Flask, render_template, request, jsonify
from predicting_salary import predictor
from database_setup import autocomplete_fetcher
from salary_analysis import get_salary_differences, format_salary
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_salary = None
    actual_salary = None
    message = None
    player_not_found = False

    if request.method == 'POST':
        #first_name = (request.form['first_name'].strip()).capitalize()
        #last_name = (request.form['last_name'].strip()).capitalize()
        full_name = request.form['player_name'].strip().capitalize()
        predicted_salary, actual_salary, actual_name = predictor(full_name)
        predicted_salary = int(predicted_salary)
        
        print(predicted_salary, actual_salary)

        if predicted_salary > actual_salary:
            diff = f"{(predicted_salary - actual_salary):,}"
            message = actual_name + " is underpaid by $" + diff + "."
        elif predicted_salary < actual_salary:
            diff = f"{(actual_salary - predicted_salary):,}"
            message = actual_name + " is overpaid by $" + diff + "."
        else:
            message = actual_name + " is paid fairly."
        if predicted_salary == 0: 
            message = "Player not found. Check spelling and try again."
            player_not_found = True
        
        predicted_salary = f"{predicted_salary:,}"
        actual_salary = f"{actual_salary:,}"
    
    # Get leaderboard data
    overpaid, underpaid = get_salary_differences()
    
    return render_template('index.html', 
                         predicted_salary=predicted_salary, 
                         actual_salary=actual_salary, 
                         message=message, 
                         player_not_found=player_not_found,
                         overpaid=overpaid,
                         underpaid=underpaid,
                         format_salary=format_salary)

@app.route('/how_does_this_work')
def how_does_this_work():
    return render_template('how_does_this_work.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    results = autocomplete_fetcher(query)
    return jsonify(results)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)

