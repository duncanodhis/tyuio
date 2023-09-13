from flask import Blueprint, jsonify, request
from models.user import User
from services.user_service import UserService

user_routes = Blueprint('user_routes', __name__)
user_service = UserService()

from flask import Blueprint, jsonify, request
from models.user import User
from services.user_service import UserService
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)


user_routes = Blueprint('user_routes', __name__)
user_service = UserService()
jwt = JWTManager()
# User authentication endpoint
@user_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Authenticate user (check username and password against database)
    user = user_service.authenticate_user(username, password)

    if user:
        # Create an access token for the authenticated user
        # access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': 'access tokrn'})
    else:
        return jsonify({'message': 'Authentication failed'}), 401

# Protected route example
@user_routes.route('/api/protected', methods=['GET'])
@jwt_required()  # Requires a valid access token to access this route
def protected():
    current_user_id = get_jwt_identity()
    user = user_service.get_user(current_user_id)
    return jsonify({'message': f'Protected resource accessed by user {user.username}'})


@user_routes.route('/api/users', methods=['GET'])
@jwt_required() 
def get_users():
    users = user_service.get_users()
    return jsonify(users)

@user_routes.route('/api/users', methods=['POST'])
@jwt_required() 
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username=username, email=email, password=password)
    user_service.create_user(user)

    return jsonify({'message': 'User created successfully'})

@user_routes.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required() 
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@user_routes.route('/api/signup', methods=['POST'])
def signup():
    try:
        # Retrieve data from the request
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already taken'}), 400

        data ={
            'username':username,
            'email':email,
            'password':password
        }
        # Handle the data as needed (e.g., store it in a database)
        user_service.create_user(data)
        #access_token = create_access_token(identity=user_id)
        # Return a success message
        return jsonify({'Access token':"access_token",'message': 'Signup successful'}), 200
    except Exception as e:
        # Handle any exceptions that may occur during signup processing
        print(f"Error during signup: {str(e)}")
        return jsonify({'message': 'Signup failed'}), 500  # You can customize the error response as needed
