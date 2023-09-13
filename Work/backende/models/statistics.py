from app import db
from datetime import datetime
class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_products = db.Column(db.Integer, nullable=False)
    total_orders = db.Column(db.Integer, nullable=False)
    total_users = db.Column(db.Integer, nullable=False)
    total_reviews = db.Column(db.Integer, nullable=False)
    total_disputes = db.Column(db.Integer, nullable=False)
    total_newsletters = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Statistic {self.id}>"
