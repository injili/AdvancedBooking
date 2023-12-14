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
            checkin=datetime.strptime(user_data.get('checkin'), '%d-%m-%Y').date(),
            checkout=datetime.strptime(user_data.get('checkout'), '%d-%m-%Y').date(),
            suite=user_data.get('suite'),
            amount=user_data.get('amount')
        )
        db.session.add(user)
        db.session.flush()
        
        for room_info in room_data:
            room = RoomBookings(
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

@app.route('/action_mods', methods=['POST'])
def action_mods():
    try:
        data = request.get_json()

        room = SuiteMods(
            room_type=data['suite'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )

        db.session.add(room)
        db.session.flush()

        pricing = PriceMods(
            suite_price=data['suiteprice'],
            extra_charge=data['extraperson'],
            bed_breakfast=data['bnb'],
            full_board=data['halfboard'],
            half_board=data['fullboard'],
            room=room
        )

        db.session.add(pricing)
        db.session.commit()

        return jsonify({'message': 'The modifications have been done successsfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/update_standard', methods=['POST'])
def update_standard():
    try :
        data = request.get_json()
        standard = None

        if data['suite'] == 'Deluxe':
            standard = StandardPricing.query.filter_by(room_type='Deluxe').first()
        else:
            standard = StandardPricing.query.filter_by(room_type='Superior').first()

        if standard:
            standard.room_type=data['suite']
            standard.suite_price=data['suiteprice']
            standard.extra_charge=data['extraperson']
            standard.bed_breakfast=data['bnb']
            standard.half_board=data['halfboard']
            standard.full_board-data['fullboard']
        else:
            new = StandardPricing(
                room_type=data['suite'],
                suite_price=data['suiteprice'],
                extra_charge=data['extraperson'],
                bed_breakfast=data['bnb'],
                half_board=data['halfboard'],
                full_board=data['fullboard']
            )
            db.session.add(new)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/get_users', methods=['GET'])
def get_users():
    users = UserTable.query.all()
    user_data = []

    for user in users:
        user_info = {
            'id': user.id,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email,
            'phone': user.phone,
            'nationality': user.nationality,
            'passport': user.passport,
            'gender': user.gender,
            'no_rooms': user.no_rooms,
            'checkin': user.checkin.strftime('%d-%m-%Y'),
            'checkout': user.checkout.strftime('%d-%m-%Y'),
            'suite': user.suite,
            'amount': user.amount,
            'rooms_booked': []
        }

        for booking in user.rooms_booked:
            room_info = {
                'adults': booking.adults,
                'preteens': booking.preteens,
                'kids': booking.kids,
                'infants': booking.infants,
                'meal_plan': booking.meal_plan
            }
            user_info['room_booked'].append(room_info)

        user_data.apend(user_info)
    return jsonify({'data': user_data})

@app.route('/get_rooms/<int:user_id>', methods=['GET'])
def get_rooms(user_id):
    user = userTable.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    rooms_data = []
    for booking in user.rooms_booked:
        room_info = {
            'adults': booking.adults,
            'preteens': booking.preteens,
            'kids': booking.kids,
            'infants': booking.infants,
            'meal_plan': booking.meal_plan
        }
        room_data.append(room_info)

    return jsonify({'data': rooms_data})

@app.route('/get_mods', methods=['GET'])
def get_mods():
    mods = SuiteMods.query.all()
    mods_data = []

    for mod in mods:
        mods_info = {
            'id': mod.id,
            'room_type': mod.room_type.strftime('%d-%m-%Y'),
            'start_date': mod.start_date.strftime('%d-%m-%Y'),
            'end_date': mod.end_date,
            'price_mods': {
                'suite_price': mod.dates_moded.suite_price,
                'extra_charge': mod.dates_moded.extra_charge,
                'bed_breakfast': mod.dates_moded.bed_breakfast,
                'full_board': mod.dates_moded.full_board,
                'half_board': mod.dates_moded.half_board
            }
        }
        mods_data.append(mods_info)

    return jsonify({'data': mods_data})

@app.route('/get_pricing', methods=['GET'])
def get_pricing():
    pricing_data = StandardPricing.query.all()
    pricing_list = []

    for pricing in pricing_data:
        pricing_info = {
            'id': pricing.id,
            'room_type': pricing.room_type,
            'suite_price': pricing.suite_price,
            'extra_charge': pricing.extra_charge,
            'bed_breakfast': pricing.bed_breakfast,
            'half_board': pricing.half_board,
            'full_board': pricing.full_board
        }
        pricing_list.append(pricing_info)

    return jsonify({'data': pricing_list})


@app.route('/get_min_available_rooms', methods=['GET'])
def get_min_available_rooms():
    try:
        checkin_date = request.args.get('checkin')
        checkout_date = request.args.get('checkout')
        suite_type = request.args.get('suite_type')

        checkin_dat = datetime.strptime(checkin_date, '%d-%m-%Y').date()
        checkout_date = datetime.strptime(checkout_date, '%d-%m-%Y').date()

        available_rooms_dict = {}

        current_date = checkin_date
        while current_date <= checkout_date:
            reservations = UserTable.query.filter(
                (UserTable.checkin <= current_date) & (UserTable.checkout >= current_date) &
                (UserTable.suite == suite_type)
            ).all()

            total_rooms_for_suite = 12 if suite_type == 'Deluxe' else 6
            reserved_rooms = sum(reservation.no_rooms for reservation in reservations)
            available_rooms = total_rooms_for_site - reserved_rooms

            available_rooms_dict[str(current_date)] = available_rooms

            current_date += timedelta(days=1)
        
        min_available_rooms = min(available_rooms_dict.values())

        return jsonify({
            'status': 'success',
            'available_rooms' : available_rooms_dict,
            'min_available_rooms': min_available_rooms
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_pricing', methods=['GET'])
def get_pricing():
    try:
        room_type = request.args.get('room_type')
        checkin_date = request.args.get('checkin')
        checkout_date = request.args.get('checkout')

        checkin_date = datetime.strptime(checkin_date, '%d-%m-%Y').date()
        checkout_date = datetime.strptime(checkout_date, '%d-%m-%Y').date()

        suite_mods_entry = SuiteMods.query.filter(
            (SuiteMods.rom_type == room_type) &
            ((SuiteMods.start_date <= checkin_date) & (SuiteMods.end_date >= checkin_date) |
             (SuiteMods.start_date <= checkout_date) & (SuiteMods.end_date >= checkout_date))
        ).first()

        if suite_mods_entry:
            prices = suite_mods_entry.dates_moded
        else:
            prices = StandardPricing.query.filter(StandardPricing.room_type == room_type).first()

        if prices:
            return jsonify({
                'status': 'success',
                'suite_price': prices.suite_price,
                'extra_charge': prices.extra_charge,
                'bed_breakfast': prices.bed_breakfast,
                'half_board': prices.half_board,
                'full_board': prices.full_board
            })
        else:
            return jsonify({'status': 'error', 'message': 'No pricing information found for the specified criteria'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(port=8888, debug=True)