from app import db
from datetime import datetime

class NewsLetterBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_token = db.Column(db.String(255), nullable=False)
    channel_id = db.Column(db.String(255), nullable=False)
    
    # Define a one-to-many relationship with Newsletter
    newsletters = db.relationship('Newsletter', backref='newsletter_bot', lazy=True)

    def __repr__(self):
        return f"<NewsLetterBot {self.id}>"

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Define a foreign key relationship with NewsLetterBot
    newsletter_bot_id = db.Column(db.Integer, db.ForeignKey('news_letter_bot.id'), nullable=True)

    def __repr__(self):
        return f"<Newsletter {self.id}>"
