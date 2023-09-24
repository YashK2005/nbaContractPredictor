from flask import Flask, render_template, request
from predicting_salary import predictor
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_salary = None
    actual_salary = None
    message = None

    if request.method == 'POST':
        first_name = request.form['first_name'].capitalize()
        last_name = request.form['last_name'].capitalize()
        full_name = first_name + " " + last_name
        predicted_salary, actual_salary = predictor(first_name, last_name)
        predicted_salary = int(predicted_salary)
        print(predicted_salary, actual_salary)

        if predicted_salary > actual_salary:
            message = full_name + " is underpaid."
        elif predicted_salary < actual_salary:
            message = full_name + " is overpaid."
        else:
            message = full_name + " is paid fairly."
        if predicted_salary == 0: message = "Player not found. Check spelling and try again."

    return render_template('index.html', predicted_salary=predicted_salary, actual_salary=actual_salary, message=message)

if __name__ == '__main__':
    app.run(debug=True)

