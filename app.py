from flask import Flask, render_template, session, request, redirect, url_for, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz
from models import db, UserTable, DeluxeRoomBookings

app = Flask(__name__)

"""
PostgreSQL database configuration
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://injili:wzEotbnKTRV4BWxJAbLIFdpqYa6AWq27@dpg-cl86f8qvokcc73ashpig-a.oregon-postgres.render.com/booking_records'
app.config['SECRET_KEY'] = '2c4fefa11c38904646a17df8ee85d3a5'
app.config['SQLALCHCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

east_african_time = pytz.timezone('Africa/Nairobi')

@app.before_request
def set_timezone():
    g.timezone = east_african_time

@app.route('/', strict_slashes=False)
def home():
    return render_template('index.html')

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.json

        user_data = data.get('user', {})
        room_data = data.get('rooms', [])

        user = UserTable(
            fname=user_data.get('fname'),
            lname=user_data.get('lname'),
            email=user_data.get('email'),
            phone=user_data.get('phone'),
            nationality=user_data.get('nationality'),
            passport=user_data.get('passport'),
            gender=user_data.get('gender'),
            no_rooms=user_data.get('no_rooms'),
            checkin=user_data.get('checkin'),
            checkout=user_data.get('checkout'),
            suite=user_data.get('suite'),
            amount=user_data.get('amount')
        )
        db.session.add(user)
        db.session.flush()
        
        for room_info in room_data:
            room = DeluxeRoomBookings(
                adults=room_info.get('adults', 0),
                preteens=room_info.get('preteens', 0),
                kids=room_info.get('kids', 0),
                infants=room_info.get('infants', 0),
                meal_plan=room_info.get('meal_plan', ''),
                user=user
            )
            db.session.add(room)

        db.session.commit()

        return jsonify({'message': 'Data stored successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__' :
    app.run(port=8888, debug=True)