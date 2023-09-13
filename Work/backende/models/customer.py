from app import db
from datetime import datetime
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    telegram_id = db.Column(db.Integer, nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)
    wallet_address = db.Column(db.String(255))
    # image = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(1000),nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    payments = db.relationship('Payment', backref='customer', lazy=True)  # Add the relationship to Payment table

    def __repr__(self):
        return f"<Customer {self.username}>"
