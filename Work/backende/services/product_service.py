from models.product import Category, Package, Product,Discount
from models.address import Address
from datetime import datetime
from app import db

class ProductService:

    def get_products(self):
        products = Product.query.all()
        product_dicts = [self._convert_to_dict(product) for product in products]
        
        # Add package image URL to each product dictionary
        for product_dict in product_dicts:
            product_dict['package_image'] = self.get_package_image(product_dict['id'])
        
        return product_dicts

    def get_package_image(self, product_id):
        product = Product.query.get(product_id)
        if product and product.package:
            return product.package.image.replace('\\', '/')
        return None
    def get_product(self, product_id):
        product = Product.query.get(product_id)
        return self._convert_to_dict(product) if product else None

    def create_product(self, data):
        # Extract the data from the input dictionary
        selling_price = data['selling_price']
        selling_currency = data['selling_currency']
        selling_description = data['selling_description']
        country = data['country']
        city = data['city']
        district = data['district']
        package_weight = data['package_weight']
        package_weight_measurement = data['package_weight_measurement']
        selling_weight = data.get('selling_weight', 0.0)
        selling_weight_measurement = data.get('selling_weight_measurement', '')
        category_id = data['category_name']
        package_id = data['product_name']
        print(category_id)
      
        category = Category.query.get(category_id)
        if not category:
            raise ValueError('Invalid category_name')

        # Retrieve the Package (Product) based on its name and category_id
        package = Package.query.filter_by(id=package_id, category_id=category.id).first()
        if not package:
            raise ValueError('Invalid package_id')
        # Retrieve the Address based on country, city, and district
        address = Address.query.filter_by(country=country, city=city, district=district).first()
        if not address:
            raise ValueError('Invalid address details')

        # Create the Product record and link it to the Category, Package, and Address
        product = Product(
            name=package.name,
            package_description=package.description,
            package_weight=package.weight,
            package_weight_measurement=package_weight_measurement,
            package_price=package.price,
            package_currency=package.currency,
            selling_description=selling_description,
            selling_price=selling_price,
            selling_currency=selling_currency,  
            selling_weight=selling_weight,
            selling_weight_measurement=selling_weight_measurement,
            country=country,
            city=city,
            district=district,
            category=category,
            package=package,
            address=address,
        )

        # Add the product to the session and commit the changes
        db.session.add(product)
        db.session.commit()

        return self._convert_to_dict(product)

    # Rest of the methods remain the same as in the previous code snippet
    def update_product(self, product_id, data):
        print("Data", data)
        product = Product.query.get(product_id)
        print("Product name", product.name)
        
        if product:
            # Update the fields based on the input data
            product.name = data.get('name', product.name)
            product.package_price = data.get('package_price', product.package_price)
            product.package_currency = data.get('package_currency', product.package_currency)
            product.package_description = data.get('package_description', product.package_description)
            product.package_weight = data.get('package_weight', product.package_weight)
            product.package_weight_measurement = data.get('package_weight_measurement', product.package_weight_measurement)
            product.selling_price = data.get('selling_price', product.selling_price)
            product.selling_currency = data.get('selling_currency', product.selling_currency)
            product.selling_weight = data.get('selling_weight', product.selling_weight)
            product.selling_weight_measurement = data.get('selling_weight_measurement', product.selling_weight_measurement)
            product.country = data.get('country', product.country)
            product.city = data.get('city', product.city)
            product.district = data.get('district', product.district)

            db.session.commit()
            return self._convert_to_dict(product)
    
        return None

    def delete_product(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
    
    def get_products_country_city_category(self, selected_country, selected_city, category_id):
        products = Product.query.filter_by(country=selected_country, city=selected_city, category_id=category_id).all()
        print(products)
        return [self._convert_to_dict(product) for product in products]
   
    def get_specific_product(self, selected_country, selected_city,selected_district, category_id, selected_product):
            # Retrieve the specific product based on country, city,district category, and package name (selected_product)
            product = Product.query.filter_by(
                country=selected_country,
                city=selected_city,
                district=selected_district,
                category_id=category_id,
                package_name=selected_product
            ).first()

            return self._convert_to_dict(product) if product else None
    
    def get_product_by_address_and_package(self, address_id, package_id):
        product = Product.query.filter_by(address_id=address_id, package_id=package_id).first()
        return self._convert_to_dict(product) if product else None

    def create_discount(self,product_id, percentage, start_date, end_date, amount, currency, number_of_purchases):
        try:
            # Parse the date strings into datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Create a new Discount object
            discount = Discount(
                product_id=product_id,
                percentage=percentage,
                start_date=start_date,
                end_date=end_date,
                amount=amount,
                currency=currency,
                number_of_purchases=number_of_purchases
            )

            # Add the discount to the database session and commit the transaction
            db.session.add(discount)
            db.session.commit()

            return discount  # Return the created discount
        except Exception as e:
            db.session.rollback()
            raise e

    def calculate_discounted_cost(total_cost, product_name, number_of_purchases):
        try:
            # Get the product by its name
            product = Product.query.filter_by(name=product_name).first()
            if product:
                # Fetch the applicable discount
                applicable_discount = Discount.query.filter(
                    Discount.product_id == product.id,
                    Discount.start_date <= datetime.utcnow(),
                    Discount.end_date >= datetime.utcnow(),
                    Discount.number_of_purchases <= number_of_purchases
                ).order_by(Discount.number_of_purchases.desc()).first()

                if applicable_discount:
                    # Calculate the discount amount
                    if applicable_discount.percentage is not None:
                        discount_amount = total_cost * (applicable_discount.percentage / 100)
                    else:
                        discount_amount = applicable_discount.amount

                    # Calculate the new total cost after discount
                    new_total_cost = total_cost - discount_amount

                    return new_total_cost
                else:
                    # No applicable discount found, return the original total cost
                    return total_cost
            else:
                # Product not found, return the original total cost
                return total_cost
        except Exception as e:
            # Handle exceptions or log errors as needed
            raise e


    def _convert_to_dict(self, product):
        if product:
            return {key: getattr(product, key) for key in product.__dict__.keys() if not key.startswith('_')}
        return None
