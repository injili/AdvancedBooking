from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class UserTable(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = dbColumn(db.String(50), nullable=False)
    email = dbColumn(db.String(100), nullable=False)
    phone = dbColumn(db.String(25), nullable=False)
    no_rooms = db.Column(db.Integer, nullable=False)
    amount = dbColumn(db.Integer, nullable=False)

class DeluxeRoomBookings(db.model):
    id = db.Column(db.integer, primary_key=True)
    adults = db.Column(db.Integer, nullable=False)
    preteens = db.Column(db.Integer, nullable=False)
    kids = db.Column(db.Integer, nullable=False)
    infants = db.Column(db.Integer, nullable=False)
    meal_plan = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    user = db.relationship('UserTable', backref('roomsbooked'))