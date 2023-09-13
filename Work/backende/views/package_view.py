from flask import Blueprint, jsonify, request
from models.product import Package
from services.package_service import PackageService

package_view = Blueprint('package_view', __name__)
package_service = PackageService()

@package_view.route('/packages', methods=['GET'])
def get_packages():
    packages = package_service.get_packages()
    return jsonify(packages)

@package_view.route('/packages', methods=['POST'])
def create_package():
    data = request.get_json()
    name = data.get('name')
    image = data.get('image')
    price = data.get('price')
    currency = data.get('currency')
    description = data.get('description')
    weight = data.get('weight')
    weight_measurement = data.get('weight_measurement')
    category_id = data.get('category_id')

    package_data = {
        'name': name,
        'image': image,
        'price': price,
        'currency': currency,
        'description': description,
        'weight': weight,
        'weight_measurement': weight_measurement,
        'category_id': category_id
    }

    try:
        created_package = package_service.create_package(package_data)
        return jsonify({'message': 'Package created successfully', 'package': created_package}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@package_view.route('/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    package = package_service.get_package(package_id)
    if package:
        return jsonify(package)
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_view.route('/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    data = request.get_json()
    updated_package = package_service.update_package(package_id, data)
    if updated_package:
        return jsonify({'message': 'Package updated successfully', 'package': updated_package})
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_view.route('/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    result = package_service.delete_package(package_id)
    if result:
        return jsonify({'message': 'Package deleted successfully'})
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_view.route('/packages/single/<int:package_id>', methods=['GET'])
def get_single_package(package_id):
    package = package_service.get_package(package_id)
    if package:
        return jsonify(package)
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_view.route('/packages/<int:package_id>/description', methods=['GET'])
def get_package_description(package_id):
    description = package_service.get_package_description(package_id)
    return jsonify(description)