from flask import Blueprint, jsonify, request
from models.product import Category
from services.category_service import CategoryService

category_routes = Blueprint('category_routes', __name__)
category_service = CategoryService()

@category_routes.route('/api/categories', methods=['GET'])
def get_categories():
    categories = category_service.get_categories()
    return jsonify(categories)

@category_routes.route('/api/categories', methods=['POST'])
def create_category():
    name = request.form.get('name')
    category = Category(name=name)
    created_category = category_service.create_category(category)
    return jsonify({'message': 'Category created successfully', 'category': created_category})

@category_routes.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = category_service.get_category(category_id)
    if category:
        return jsonify(category)
    else:
        return jsonify({'message': 'Category not found'}), 404

@category_routes.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    updated_category = category_service.update_category(category_id, data)
    if updated_category:
        return jsonify({'message': 'Category updated successfully', 'category': updated_category})
    else:
        return jsonify({'message': 'Category not found'}), 404

@category_routes.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    result = category_service.delete_category(category_id)
    if result:
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404
    
@category_routes.route('/api/countries/<string:selected_country>/cities/<string:selected_city>/categories', methods=['GET'])
def get_categories_in_city(selected_country, selected_city):
    # Here, you can use the selected_country and selected_city variables to fetch categories in the selected city
    # For example, assuming you have a function in the CategoryService to get categories in a specific city,
    # you can use it as follows:
    categories = category_service.get_categories_in_city(selected_country, selected_city)
    if categories:
        return jsonify(categories)
    else:
        return jsonify({'message': f'No categories found in {selected_city}'}), 404