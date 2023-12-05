from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add')
def add_record():
    new_record = None

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone_no']
        nationality = request.form['nationality']
        passport = request.form['passport']
        gender = request.form['gender']
        no_rooms = request.form['no_rooms']
        check_in = request.form['checkin']
        check_out = request.form['checkout']
        grandtotal = request.form['cost']

if __name__ == '__main__' :
    app.run(port=8888, debug=True)