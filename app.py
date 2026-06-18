from flask import Flask, render_template, request, jsonify, redirect, url_for
from predicting_salary import predictor
from database_setup import autocomplete_fetcher
from salary_analysis import get_salary_differences, format_salary
import os

app = Flask(__name__, static_folder='public/static', static_url_path='/static')

def get_prediction_result(full_name):
    predicted_salary, actual_salary, actual_name = predictor(full_name)
    predicted_salary = int(predicted_salary)

    if predicted_salary == 0:
        return {
            "found": False,
            "message": "Player not found. Check the spelling and try again.",
            "predicted_salary": "0",
            "actual_salary": "0",
            "player_name": ""
        }

    if predicted_salary > actual_salary:
        diff = f"{(predicted_salary - actual_salary):,}"
        message = actual_name + " is underpaid by $" + diff + "."
    elif predicted_salary < actual_salary:
        diff = f"{(actual_salary - predicted_salary):,}"
        message = actual_name + " is overpaid by $" + diff + "."
    else:
        message = actual_name + " is paid fairly."

    return {
        "found": True,
        "message": message,
        "predicted_salary": f"{predicted_salary:,}",
        "actual_salary": f"{actual_salary:,}",
        "player_name": actual_name
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_salary = None
    actual_salary = None
    message = None
    player_not_found = False
    clear_result_on_refresh = False

    if request.method == 'POST':
        full_name = request.form['player_name'].strip()
        if not full_name:
            return redirect(url_for('index'))
        return redirect(url_for('index', player_name=full_name))

    full_name = request.args.get('player_name', '').strip()
    if full_name:
        clear_result_on_refresh = True
        result = get_prediction_result(full_name)
        player_not_found = not result["found"]
        message = result["message"]
        predicted_salary = result["predicted_salary"]
        actual_salary = result["actual_salary"]
    
    # Get leaderboard data
    overpaid, underpaid = get_salary_differences()
    
    return render_template('index.html', 
                         predicted_salary=predicted_salary, 
                         actual_salary=actual_salary, 
                         message=message, 
                         player_not_found=player_not_found,
                         clear_result_on_refresh=clear_result_on_refresh,
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

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.svg'), code=308)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    full_name = data.get('player_name', '').strip()
    if not full_name:
        return jsonify({
            "found": False,
            "message": "Enter a player name.",
            "predicted_salary": "0",
            "actual_salary": "0",
            "player_name": ""
        }), 400

    return jsonify(get_prediction_result(full_name))

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
