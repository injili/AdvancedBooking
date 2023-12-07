from flask_sqlalchemy import SQLAlchemy
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
    checkin = db.Column(db.DateTime, nullable=False)
    checkout = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    rooms_booked = db.relationship('DeluxeRoomBookings', backref='user', lazy=True)

class DeluxeRoomBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adults = db.Column(db.Integer, nullable=False)
    preteens = db.Column(db.Integer, nullable=False)
    kids = db.Column(db.Integer, nullable=False)
    infants = db.Column(db.Integer, nullable=False)
    meal_plan = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)