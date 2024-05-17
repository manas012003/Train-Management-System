from flask import Blueprint, request, jsonify
from models import db, User, Train, Booking
from utils import admin_required, login_required
from flask_jwt_extended import create_access_token, get_jwt_identity

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity={'id': user.id, 'username': user.username, 'is_admin': user.is_admin})
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/add_train', methods=['POST'])
@admin_required
def add_train():
    data = request.get_json()
    train = Train(
        source=data.get('source'),
        destination=data.get('destination'),
        total_seats=data.get('total_seats'),
        available_seats=data.get('total_seats')
    )
    db.session.add(train)
    db.session.commit()
    return jsonify({'message': 'Train added successfully'}), 201

@bp.route('/trains', methods=['GET'])
@login_required
def get_trains():
    source = request.args.get('source')
    destination = request.args.get('destination')
    trains = Train.query.filter_by(source=source, destination=destination).all()
    return jsonify([{
        'id': train.id,
        'source': train.source,
        'destination': train.destination,
        'total_seats': train.total_seats,
        'available_seats': train.available_seats
    } for train in trains]), 200

@bp.route('/book_seat', methods=['POST'])
@login_required
def book_seat():
    data = request.get_json()
    train_id = data.get('train_id')
    seats_requested = data.get('seats_requested', 1)
    current_user = get_jwt_identity()

    train = Train.query.filter_by(id=train_id).first()
    if train and train.available_seats >= seats_requested:
        train.available_seats -= seats_requested
        booking = Booking(user_id=current_user['id'], train_id=train_id, seats_booked=seats_requested)
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': 'Booking successful'}), 201
    return jsonify({'message': 'Not enough seats available'}), 400

@bp.route('/booking_details/<int:booking_id>', methods=['GET'])
@login_required
def get_booking_details(booking_id):
    booking = Booking.query.filter_by(id=booking_id).first()
    if booking:
        return jsonify({
            'id': booking.id,
            'user_id': booking.user_id,
            'train_id': booking.train_id,
            'seats_booked': booking.seats_booked
        }), 200
    return jsonify({'message': 'Booking not found'}), 404
