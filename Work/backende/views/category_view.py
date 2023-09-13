from flask import Blueprint, jsonify, request
from models.product import Category
from services.category_service import CategoryService

category_view = Blueprint('category_view', __name__)
category_service = CategoryService()

@category_view.route('/api/categories', methods=['GET'])
def get_categories():
    categories = category_service.get_categories()
    return jsonify(categories)


@category_view.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')

    category_data = {
        'name': name,
    }

    created_category = category_service.create_category(category_data)
    return jsonify({'message': 'Category created successfully', 'category': created_category})

@category_view.route('/api/categories/<string:category_name>', methods=['GET'])
def get_category_by_name(category_name):
    category = category_service.get_category_by_name(category_name)
    if category:
        return jsonify(category)
    else:
        return jsonify({'message': 'Category not found'}), 404

@category_view.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    updated_category = category_service.update_category(category_id, data)
    if updated_category:
        return jsonify({'message': 'Category updated successfully', 'category': updated_category})
    else:
        return jsonify({'message': 'Category not found'}), 404

@category_view.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    result = category_service.delete_category(category_id)
    if result:
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404
