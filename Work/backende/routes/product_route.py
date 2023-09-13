from flask import Blueprint, jsonify, request, current_app
from services.address_service import AddressService
from services.product_service import ProductService
from services.package_service import PackageService
from flask import send_from_directory
import os
from datetime import datetime
from app import db  # Import your db instance
from models.product import Product  # Import the Product model
from werkzeug.utils import secure_filename
from models.customer import Customer

product_routes = Blueprint('product_routes', __name__)
address_service = AddressService()
product_service = ProductService()
package_service = PackageService()
# uploads_dir = os.path.join(os.path.dirname(__file__))

@product_routes.route('/api/products', methods=['GET'])
def get_products():
    products = product_service.get_products()
    return jsonify(products)

@product_routes.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    category_name = data.get('category')
    package_name = data.get('package')
    package_price = data.get('package_price')
    package_currency = data.get('package_currency')
    package_weight = data.get('weight')
    package_weight_measurement = data.get('package_measurement')
    package_description = data.get('stockPackageDescription')
    selling_price = data.get('selling_price')
    selling_currency = data.get('selling_currency')
    selling_description = data.get('sellingDescription')
    selling_weight = data.get('selling_weight')
    selling_weight_measurement = data.get('selling_measurement')

    country = data.get('country')
    city = data.get('city')
    district = data.get('district')

    # Code to create the product_data dictionary
    product_data = {
        'category_name': category_name,
        'product_name': package_name,
        'selling_price': selling_price,
        'selling_currency': selling_currency,
        'selling_description': selling_description,
        'country': country,
        'city': city,
        'district': district,
        'package_description': package_description,
        'package_price': package_price,
        'package_currency': package_currency,
        'package_weight': package_weight,
        'package_weight_measurement': package_weight_measurement,
        'selling_weight': selling_weight,
        'selling_weight_measurement': selling_weight_measurement,
    }

    # Code to create the product using the ProductService
    created_product = product_service.create_product(product_data)
    return jsonify({'message': 'Product created successfully', 'product': created_product}), 201

@product_routes.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = product_service.get_product(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_routes.route('/api/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    try:
        data = request.form

        # Fetch the product from the database
        product = Product.query.get(product_id)
        # Update the product fields based on received data
        product.package_name = data.get('package_name')
        product.package_price = data.get('package_price')
        product.package_currency = data.get('package_currency')
        product.selling_price = data.get('selling_price')
        product.selling_weight = data.get('selling_weight')
        product.selling_weight_measurement = data.get('selling_weight_measurement')
        product.package_description = data.get('package_description')
        product.country = data.get('country')
        product.city = data.get('city')
        product.district = data.get('district')

        # Get the uploaded image file
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path_on_server = os.path.join(upload_folder, filename)
            image_file.save(image_path_on_server)
            product.package.image = image_path_on_server
        
        # Commit changes to the database
        db.session.commit()
        # Return a success response
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        # Handle any errors that might occur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product_routes.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = product_service.delete_product(product_id)
    if result:
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_routes.route('/api/countries/<string:selected_country>/cities/<string:selected_city>/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_country_city_category(selected_country, selected_city, category_id):
    products = product_service.get_products_country_city_category(selected_country, selected_city, category_id)
    return jsonify(products)

@product_routes.route('/api/countries/<string:selected_country>/cities/<string:selected_city>/categories/<int:category_id>/products/<int:selected_product>', methods=['GET'])
def get_specific_product(selected_country, selected_city, category_id, selected_product):
    product = product_service.get_specific_product(selected_country, selected_city, category_id, selected_product)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404
    
@product_routes.route('/api/product/<int:address_id>/<int:package_id>', methods=['GET'])
def get_product_by_address_and_package(address_id, package_id):
    product = product_service.get_product_by_address_and_package(address_id, package_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404


@product_routes.route('/api/customer-discount', methods=['POST'])
def create_customer_discount():
    data = request.get_json()
    customer_id = data.get('customer_id')
    discount_amount = data.get('discount_amount')

    # Check if the customer with the given ID exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # Validate the discount amount (e.g., ensure it's a positive number)
    if discount_amount <= 0:
        return jsonify({'message': 'Discount amount must be a positive number'}), 400

    # For example, you can update the customer's discount amount
    customer.discount_amount = discount_amount
    db.session.commit()

    return jsonify({'message': 'Customer discount data saved successfully'}), 200


@product_routes.route('/api/product-discount', methods=['POST'])
def create_product_georgian_currency():
    data = request.get_json()
    product_id = data.get('product_id')
    discount_amount = data.get('discount_amount')

    # Check if the product with the given ID exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Validate the discount amount (e.g., ensure it's a positive number)
    if discount_amount <= 0:
        return jsonify({'message': 'discount amount must be a positive number'}), 400

    # Process the product discount  data
    # You can save it to the database or perform any other actions here

    # For example, you can update the product's discount amount
    product.discount_amount = discount_amount
    db.session.commit()

    return jsonify({'message': 'Product Georgian currency data saved successfully'}), 200

import re
@product_routes.route('/image/<path:file_name>')
def get_image_path(file_name):
  """Retrieves and returns the path of the image file.

  Args:
    file_name: The name of the image file.

  Returns:
    The path of the image file as a string.
  """

  import os
  import pathlib

  # Get the current working directory.
  current_dir = os.getcwd()

  # Create a pathlib object for the image file.
  image_path = pathlib.Path(current_dir, file_name)

  # Check if the image file exists.
  if not image_path.is_file():
    raise FileNotFoundError(f"The file '{file_name}' does not exist.")

  # Convert the WindowsPath object to a string.
  image_path_str = str(image_path)
  print("image path",image_path)
  return image_path_str

@product_routes.route('/api/discount', methods=['POST'])
def add_discount():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract data fields
        product_id = data.get('productId')
        percentage = data.get('discountPercentage')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        amount = data.get('amountOfPurchases')
        currency = data.get('currency')
        number_of_purchases = data.get('numberOfPurchases')

        discount = product_service.create_discount(product_id, percentage, start_date, end_date, amount, currency, number_of_purchases)

        return jsonify({'message': 'Discount created successfully', 'discount_id': discount.id}), 201
    except Exception as e:
        print("Error",e)
        return jsonify({'error': 'Failed to create discount', 'message': str(e)}), 500


@product_routes.route('/api/calculate_discount', methods=['POST'])
def calculate_discount():
    try:
        # Get data from the request JSON
        data = request.get_json()

        # Extract data fields
        total_cost = data.get('total_cost')
        product_name = data.get('product_name')
        number_of_purchases = data.get('number_of_purchases')
        # Calculate the discounted cost
        discounted_cost = product_service.calculate_discounted_cost(total_cost, product_name, number_of_purchases)
        # Return the result as JSON response
        return jsonify({'discounted_cost': discounted_cost}), 200
    except Exception as e:
        # Handle exceptions or log errors as needed
        return jsonify({'error': 'Failed to calculate discount', 'message': str(e)}), 500

