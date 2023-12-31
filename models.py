from flask_sqlalchemy import SQLAlchemy
from datetime import date
db = SQLAlchemy()

class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    passport = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    no_rooms = db.Column(db.Integer, nullable=False)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    suite = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    rooms_booked = db.relationship('RoomBookings', backref='user', lazy=True)

class RoomBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adults = db.Column(db.Integer, nullable=False)
    preteens = db.Column(db.Integer, nullable=False)
    kids = db.Column(db.Integer, nullable=False)
    infants = db.Column(db.Integer, nullable=False)
    meal_plan = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)

class SeasonalPricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(25), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    suite_price = db.Column(db.Integer, nullable=False)
    extra_charge = db.Column(db.Integer, nullable=False)
    bed_breakfast = db.Column(db.Integer, nullable=False)
    full_board = db.Column(db.Integer, nullable=False)
    half_board = db.Column(db.Integer, nullable=False)

class StandardPricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(25), nullable=False)
    suite_price = db.Column(db.Integer, nullable=False)
    extra_charge = db.Column(db.Integer, nullable=False)
    bed_breakfast = db.Column(db.Integer, nullable=True)
    half_board = db.Column(db.Integer, nullable=False)
    full_board = db.Column(db.Integer, nullable=False)