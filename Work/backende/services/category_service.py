from models.product import Category 
from models.product import Product 
from app import db

class CategoryService:
    def get_categories(self):
        categories = Category.query.all()
        return [self._convert_to_dict(category) for category in categories]

    def get_category(self, category_id):
        category = Category.query.get(category_id)
        return self._convert_to_dict(category) if category else None
    
    def get_category_by_name(self, category_name):
        category = Category.query.filter_by(name=category_name).first()
        return category.id if category else None
    
    def create_category(self, data):
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        return self._convert_to_dict(category)

    def update_category(self, category_id, data):
        category = Category.query.get(category_id)
        if category:
            for key, value in data.items():
                setattr(category, key, value)
            db.session.commit()
            return self._convert_to_dict(category)
        return None

    def delete_category(self, category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
    def get_categories_in_city(self, selected_country, selected_city):
        # Fetch categories in the specified city
        categories = Category.query.join(Product).filter(Product.country == selected_country, Product.city == selected_city).all()
        return [self._convert_to_dict(category) for category in categories]


    def _convert_to_dict(self, category):
        if category:
            return {key: getattr(category, key) for key in category.__dict__.keys() if not key.startswith('_')}
        return None
