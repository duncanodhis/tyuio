from flask import Blueprint, jsonify, request, current_app
from models.product import Package
from services.package_service import PackageService
from services.category_service import CategoryService
import os
from flask import send_file

package_routes = Blueprint('package_routes', __name__)
package_service = PackageService()
category_service = CategoryService()

@package_routes.route('/api/packages', methods=['GET'])
def get_packages():
    packages = package_service.get_packages()
    return jsonify(packages)

@package_routes.route('/api/packages', methods=['POST'])
def create_package():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'image' not in request.files:
        return jsonify({'error': 'Image must be provided.'}), 400

    name = request.form.get('name')
    price = request.form.get('price')
    currency = request.form.get('currency')
    description = request.form.get('description')
    weight = request.form.get('weight')
    weight_measurement = request.form.get('weight_measurement')
    category_name = request.form.get('category_name')  # Assuming you are sending the category_name instead of category_id
    
    category_id = category_service.get_category_by_name(category_name)
    # print("cat",category_id)
    image = request.files['image']
    image.save(os.path.join(upload_folder, image.filename))
    image_path = os.path.join(upload_folder, image.filename)

    package_data = {
        'name': name,
        'price': price,
        'currency': currency,
        'description': description,
        'weight': weight,
        'weight_measurement': weight_measurement,
        'category_id': category_id,  
        'image': image_path
    }

    try:
        created_package = package_service.create_package(package_data)
        return jsonify({'message': 'Package created successfully', 'package': created_package}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@package_routes.route('/api/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    package = package_service.get_package(package_id)
    if package:
        return jsonify(package)
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_routes.route('/api/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    data = request.get_json()
    updated_package = package_service.update_package(package_id, data)
    if updated_package:
        return jsonify({'message': 'Package updated successfully', 'package': updated_package})
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_routes.route('/api/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    result = package_service.delete_package(package_id)
    if result:
        return jsonify({'message': 'Package deleted successfully'})
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_routes.route('/api/packages/category/<int:category_id>', methods=['GET'])
def get_packages_by_category(category_id):
    packages = package_service.get_packages_by_category_id(category_id)
    return jsonify(packages)

@package_routes.route('/api/packages/single/<int:package_id>', methods=['GET'])
def get_single_package(package_id):
    package = package_service.get_package_by_id(package_id)
    if package:
        return jsonify(package)
    else:
        return jsonify({'message': 'Package not found'}), 404

@package_routes.route('/api/packages/<int:package_id>/description', methods=['GET'])
def get_package_description(package_id):

    description = package_service.get_package_description(package_id)
    return jsonify(description)


@package_routes.route('/api/packages/<int:id>/photo', methods=['GET'])
def get_product_photo(id):
    # Retrieve product photo path based on country and city
    product_photo_path = package_service.get_product_photo_path(id)
    print(product_photo_path)
    if product_photo_path:
        # Return the image file as a response
        return send_file(product_photo_path, mimetype='image/jpeg')
    else:
        return jsonify({'message': 'Product photo not found'}), 404
