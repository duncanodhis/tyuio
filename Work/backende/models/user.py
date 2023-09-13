from datetime import datetime
from app import db
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


class ShopBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<ShopTelegramBot {self.id}>"

class CourierBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<CourierTelegramBot {self.id}>"

class DisputesReviewsBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<DisputesReviewsBot {self.id}>"

class NewsletterChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<NewsletterChannel {self.id}>"
