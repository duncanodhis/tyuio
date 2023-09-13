from flask import Blueprint, jsonify, request
from models.user import User
from services.user_service import UserService

user_view = Blueprint('user_view', __name__)
user_service = UserService()

@user_view.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_users()
    return jsonify(users)

@user_view.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username=username, email=email, password=password)
    created_user = user_service.create_user(user)
    return jsonify({'message': 'User created successfully', 'user': created_user})

@user_view.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@user_view.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = user_service.update_user(user_id, data)
    if updated_user:
        return jsonify({'message': 'User updated successfully', 'user': updated_user})
    else:
        return jsonify({'message': 'User not found'}), 404

@user_view.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_service.delete_user(user_id)
    if result:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404
