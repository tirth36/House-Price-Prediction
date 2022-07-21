import os.path

import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import util

app = Flask(__name__, template_folder=os.path.abspath('../client'))
CORS(app)

app.secret_key = 'Jay@#112233'


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def get_homepage():
    if session.get("loggedin") is None:
        return redirect('/login')
    else:
        return render_template('index.html')


@app.route('/predict-price', methods=['GET'])
def get_prediction_page():
    return render_template('prediction.html')


@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def get_register_page():
    return render_template('register.html')


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/python_register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    # Show registration form with message (if any)
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    # If account exists show error and validation checks
    if account:
        msg = 'Account already exists!'
    else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
    return msg


@app.route('/python_login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Show registration form with message (if any)
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))

    account = cursor.fetchone()
    # If account exists show error and validation checks
    if account:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        msg = "0"
    else:
        msg = "1"
    return msg


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
