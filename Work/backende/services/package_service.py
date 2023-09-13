from app import db
from models.product import Category
from models.product import Package

class PackageService:
    def get_packages(self):
        packages = Package.query.all()
        return [self._convert_to_dict(package) for package in packages]

    def get_package(self, package_id):
        package = Package.query.get(package_id)
        return self._convert_to_dict(package) if package else None

    def create_package(self, data):
        category_id = data.pop('category_id', None)
        category = Category.query.get(category_id)
        if not category:
            raise ValueError('Invalid category_id')

        package = Package(**data)
        package.category = category

        db.session.add(package)
        db.session.commit()
        return self._convert_to_dict(package)

    def update_package(self, package_id, data):
        package = Package.query.get(package_id)
        if not package:
            return None

        category_id = data.pop('category_id', None)
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                raise ValueError('Invalid category_id')
            package.category = category

        for key, value in data.items():
            setattr(package, key, value)

        db.session.commit()
        return self._convert_to_dict(package)

    def delete_package(self, package_id):
        package = Package.query.get(package_id)
        if package:
            db.session.delete(package)
            db.session.commit()
            return True
        return False
    
    def get_packages_by_category_id(self, category_id):
        packages = Package.query.filter_by(category_id=category_id).all()
        return [self._convert_to_dict(package) for package in packages]

    def get_package_by_id(self, package_id):
        package = Package.query.get(package_id)
        return self._convert_to_dict(package) if package else None
    
    def get_package_description(package_id):
        package = Package.query.get(package_id)
        if package:
            return {'description': package.package_description}
        else:
            return {'description': 'Package not found'}
    def get_product_photo_path(self, id):
        # Query the database to get the city photo path
        package = Package.query.filter_by(id = id).first()
        if package:
            return package.image
        return None
    def _convert_to_dict(self, package):
        if package:
            return {key: getattr(package, key) for key in package.__dict__.keys() if not key.startswith('_')}
        return None
      

