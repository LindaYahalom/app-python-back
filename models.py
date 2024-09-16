# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

db = SQLAlchemy()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_subscribed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, budget, email):
        self.name = name
        self.budget = budget
        self.email = email.lower()

    def __repr__(self):
        return f'<Subscriber {self.email}>'

    @staticmethod
    def is_valid_email(email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

# Booking Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.String(100), nullable=False)
    endDate = db.Column(db.String(100), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Booking {self.name} to {self.destination}>'
    

    # Destination Model
class Destination(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    banner_image = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    teaser = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    gallery_images = db.Column(db.Text, nullable=False)  # Store as comma-separated strings
    events = db.Column(db.Text, nullable=False)  # Store as JSON string

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bannerImage": self.banner_image,
            "image": self.image,
            "teaser": self.teaser,
            "description": self.description,
            "galleryImages": self.gallery_images.split(','),  # Split comma-separated values into a list
            "events": eval(self.events)  # Convert stored string back to dictionary
        }