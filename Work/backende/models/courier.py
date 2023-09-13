from app import db
from models.product import Product

class Courier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='courier', lazy=True)
    total_earning = db.Column(db.Float, default=0.0)
    commission_currency = db.Column(db.String(200), nullable=True)  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    area_of_distribution = db.Column(db.String(10000), nullable=False)
    commission = db.Column(db.Float, nullable=False)
    commission_currency = db.Column(db.String(200), nullable=False)
    cost_of_item = db.Column(db.Float, nullable=False)
    weight_of_item = db.Column(db.Float, nullable=False)
    item_weight_measurement = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    number_of_items = db.Column(db.Float, nullable=False)
    number_of_treasures = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Remove the foreign key reference to Treasure
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    product = db.relationship('Product', backref=db.backref('products', lazy=True))

class Treasure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=True)
    coordinates = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    taken = db.Column(db.Boolean, default=False)

    # Maintain the relationship to Task without a foreign key reference
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('treasures', lazy=True))
