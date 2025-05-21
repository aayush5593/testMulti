from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

# Initialize Flask app and configure DB
app = Flask(__name__, template_folder='Templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@db:5432/logsdb'
db = SQLAlchemy(app)

# Route for the calculator home page
@app.route('/')
def index():
    return render_template('CalcFront.html')

# Log model to store calculation logs
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    data = db.Column(db.Text, nullable=False)

# Route to perform calculation
@app.route('/Calculating', methods=['POST'])
def Calculating():
    number1 = float(request.form['num1'])
    number2 = float(request.form['num2'])
    operation = request.form['operation']

    if operation == 'add':
        result = number1 + number2
    elif operation == 'subtract':
        result = number1 - number2
    elif operation == 'multiply':
        result = number1 * number2
    elif operation == 'divide':
        result = number1 / number2
    else:
        result = "Invalid operation"

    # Log the operation
    timestamp = datetime.datetime.now().isoformat()
    log_entry = Log(timestamp=timestamp, data=f"Operation: {operation}, Num1: {number1}, Num2: {number2}, Result: {result}")
    db.session.add(log_entry)
    db.session.commit()

    return render_template('CalcFront.html', result=result)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
