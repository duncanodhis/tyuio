from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    number_of_orders = db.Column(db.Integer,nullable = False)
    quantity_unit=db .Column(db.String(1000), nullable=False)
    total_price = db.Column(db.Float, nullable=False)   
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    telegram_id = db.Column(db.Integer, db.ForeignKey('customer.telegram_id'), nullable=False)
    transaction_id = db.Column(db.String, db.ForeignKey('payment.transaction_id'), nullable=False)
    treasure_id = db.Column(db.Integer, db.ForeignKey('treasure.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship('Payment', backref=db.backref('orders', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))
    treasure = db.relationship('Treasure', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"<Order {self.id}>"
