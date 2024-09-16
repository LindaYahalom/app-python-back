# app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from flask_cors import CORS
from config import Config
from models import db, Subscriber, Booking, Destination
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
mail = Mail(app)
CORS(app)  # Enable CORS to allow requests from your Next.js frontend

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    name = data.get('name')
    budget = data.get('budget')
    email = data.get('email')

    # Validate data
    if not name or not budget or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    if not Subscriber.is_valid_email(email):
        return jsonify({'error': 'Invalid email address'}), 400

    # Check if email already exists
    existing_subscriber = Subscriber.query.filter_by(email=email.lower()).first()
    if not existing_subscriber:
        # Add subscriber to database
        new_subscriber = Subscriber(name=name, budget=budget, email=email)
        db.session.add(new_subscriber)
        db.session.commit()



    # Send confirmation email
    send_confirmation_email(email, name)

    return jsonify({'message': 'Subscription successful! Please check your email for confirmation.'}), 200

def send_confirmation_email(recipient_email, recipient_name):
    msg = Message('Subscription Confirmation',
                  recipients=[recipient_email])
    msg.body = f'Dear {recipient_name},\n\nThank you for subscribing to our newsletter!'
    mail.send(msg)

@app.route('/api/book', methods=['POST'])
def book():
    data = request.get_json()

    # Extract data from the request
    name = data.get('name')
    destination = data.get('destination')
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    passengers = data.get('passengers')

    # Validate input
    if not name or not destination or not endDate or not startDate or not passengers:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new booking instance
    new_booking = Booking(name=name, destination=destination, startDate=startDate, endDate=endDate, passengers=passengers)
    db.session.add(new_booking)
    db.session.commit()

    # Return the booking information to the frontend
    return jsonify({
        'name': new_booking.name,
        'destination': new_booking.destination,
        'startDate': new_booking.startDate,
        'endDate': new_booking.endDate,
        'passengers': new_booking.passengers
    }), 200

# Route to fetch all destinations
@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# Route to fetch a single destination by id
@app.route('/api/destination/<string:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    return jsonify(destination.to_dict())

# Route to serve static images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

if __name__ == '__main__':
    app.run(debug=True)
