from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    city_image = db.Column(db.String(255))  # Column to store the city image filename or path
    district = db.Column(db.String(100), nullable=False)
    district_image = db.Column(db.String(255))  # Column to store the district image filename or path

    def __repr__(self):
        return f"<Address {self.id}>"
