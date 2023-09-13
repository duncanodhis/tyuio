from flask import Blueprint, jsonify, request
from models.product import Product
from services.product_service import ProductService

product_view = Blueprint('product_view', __name__)
product_service = ProductService()

@product_view.route('/products', methods=['GET'])
def get_products():
    products = product_service.get_products()
    return jsonify(products)

@product_view.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_category = data.get('category_name')
    product_name = data.get('product_name')
    selling_price = data.get('selling_price')
    selling_currency = data.get('selling_currency')
    country = data.get('country')
    city = data.get('city')
    district = data.get('district')
    package_description = data.get('package_description')
    selling_description = data.get('selling_description')
    package_price = data.get('package_price')
    package_currency = data.get('package_currency')
    package_weight = data.get('package_weight')
    package_weight_measurement = data.get('package_weight_measurement')
    selling_weight = data.get('selling_weight')
    selling_weight_measurement = data.get('selling_weight_measurement')

    product_data = {
        'product_name': product_name,
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
        'category_name': product_category,
    }

    created_product = product_service.create_product(product_data)
    return jsonify({'message': 'Product created successfully', 'product': created_product})

@product_view.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = product_service.get_product(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_view.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    updated_product = product_service.update_product(product_id, data)
    if updated_product:
        return jsonify({'message': 'Product updated successfully', 'product': updated_product})
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_view.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = product_service.delete_product(product_id)
    if result:
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404
