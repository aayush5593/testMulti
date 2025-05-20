from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/logsdb'
db = SQLAlchemy(app)


Calc1 = Flask(__name__, template_folder='Templates')

@Calc1.route('/')
def index():
    return render_template('CalcFront.html')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    data = db.Column(db.Text, nullable=False)


@Calc1.route('/Calculating', methods=['POST'])
def Calculating():
    
    number1 = float(request.form['num1'])
    number2 =float(request.form['num2'])
    operation = request.form['operation']

    if operation == 'add':
        result = number1 + number2

    elif operation == 'subtract':
        result = number1 - number2

    elif operation == 'multiply':
        result = number1 * number2

    elif operation == 'divide':
        result = number1 / number2

    return render_template('CalcFront.html', result=result)
    import datetime

    # Inside Calculating()
    timestamp = datetime.datetime.now().isoformat()
    log_entry = Log(timestamp=timestamp, data=f"Operation: {operation}, Num1: {number1}, Num2: {number2}, Result: {result}")
    db.session.add(log_entry)
    db.session.commit()

if __name__ == '__main__':
        Calc1.run(debug=True, host='0.0.0.0', port=8070)
