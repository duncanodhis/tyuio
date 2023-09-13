from app import db
from datetime import datetime
class Dispute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('customer.telegram_id'), nullable=False)
    urgency =db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref=db.backref('disputes', lazy=True))
    user = db.relationship('Customer', backref=db.backref('disputes', lazy=True))

    def __repr__(self):
        return f"<Dispute {self.id}>"
