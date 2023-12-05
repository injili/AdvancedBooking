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

@app.route('/store_rooms')
def store_rooms():
    data = request.json
    rooms_data = data.get('rooms')
    
    for room_info in room_data:
        room = DeluxeRoomBookings(
            adults=room_info['adults'],
            preteens=room_info['preteens'],
            kids=room_info['kids'],
            infants=room_info_info['infants'],
            meal_plan=room_info['meal_plan']
        )
        db.session.add(room)

    db.session.commit()
    return jsonify({'message': 'Rooms stored successfully'})


if __name__ == '__main__' :
    app.run(port=8888, debug=True)