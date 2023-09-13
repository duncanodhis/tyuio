from datetime import datetime
from app import db
from app import db
from models.address import Address
from models.customer import Customer
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Category {self.name}>"

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255)) 
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False) 
    description = db.Column(db.Text, nullable=False)  # Corrected the typo here
    weight = db.Column(db.Float, nullable=False)
    weight_measurement = db.Column(db.String(20), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    category = db.relationship('Category', backref=db.backref('packages', lazy=True))

    def __repr__(self):
        return f"<Package {self.name}>"

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    percentage = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    number_of_purchases = db.Column(db.Integer, nullable=True)

    product = db.relationship('Product', backref=db.backref('discounts', lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    package_description = db.Column(db.Text, nullable=False)
    selling_description = db.Column(db.Text, nullable=False)

    package_price = db.Column(db.Float, nullable=False)
    package_currency = db.Column(db.String(10), nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    selling_currency = db.Column(db.String(10), nullable=False)

    package_weight = db.Column(db.Float, nullable=False)
    package_weight_measurement = db.Column(db.String(20), nullable=False)

    selling_weight = db.Column(db.Float, nullable=False)
    selling_weight_measurement = db.Column(db.String(20), nullable=False)
    
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20),nullable = False)
    district = db.Column(db.String(20),nullable = False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    # Relationships
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    package = db.relationship('Package', backref=db.backref('products', lazy=True))
    address = db.relationship('Address', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"<Product {self.name}>"


