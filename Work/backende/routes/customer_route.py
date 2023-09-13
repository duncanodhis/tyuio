from flask import Blueprint, jsonify, request,current_app
from services.customer_service import CustomerService
import os
import requests
from block_io import BlockIo

# Initialize Block.io with your API key and version
# block_io = BlockIo(current_app.config['BLOCK_IO_API_KEY'], current_app.config['BLOCK_IO_API_VERSION'])

version = 2 # API version
block_io = BlockIo('9c46-581f-5438-412f', 'Summer2023BreezeBeach', version)

customer_routes = Blueprint('customer_routes', __name__)
customer_service = CustomerService()

@customer_routes.route('/api/customers', methods=['GET'])
def get_customers():
    customer = customer_service.get_customers()
    return jsonify(customer)

@customer_routes.route('/api/clients', methods=['GET'])
def get_customer_data():
    try:
        # Get the list of customers from your database
        customers = customer_service.get_customer_data()
        
        # Create a list to store the formatted customer data
        formatted_customer_data = []

        for customer in customers:
            # Get the Telegram ID of the customer
            telegram_id = customer['Telegram ID']
            
            # Check if the customer has a wallet address in your database
            if 'wallet_address' in customer and customer['wallet_address']:
                wallet_address = customer['wallet_address']

                # Query Block.io to get the balance for the wallet address
                balance_response = block_io.get_address_balance(addresses=wallet_address)

                if 'available_balance' in balance_response['data']:
                    available_balance = float(balance_response['data']['available_balance'])
                else:
                    available_balance = 0.0

                # Add the available balance to the customer data
                customer['Balance'] = available_balance
            
            formatted_customer_data.append(customer)
        
        return jsonify(formatted_customer_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_routes.route('/api/customersDetails', methods=['GET'])
def get_customersDetails():
    customers = customer_service.get_customers()
    print(customers)
    
    # Create a list of dictionaries with the required format
    customer_data = []
    for customer in customers:
        customer_entry = {
            "id": customer['id'],  # Access 'id' from the dictionary
            "count": len(customers),  # Total customer count remains constant for each entry
            "label": customer['created_at'].strftime('%B %Y')
        }
        customer_data.append(customer_entry)
    
    return jsonify(customer_data)

@customer_routes.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    password = data.get('password')
    print("telegram_id",telegram_id)

    # Call the /create_wallet route to create a new wallet for the customer
    create_wallet_response = requests.post(
        f'http://127.0.0.1:5000/api/create_wallet',
        json={'telegram_id': str(telegram_id)}
    )
    # created_customer = customer_service.create_customer(customer_data)
    if create_wallet_response.status_code == 200:
            # If the wallet creation was successful, extract the wallet address from the response
            image_path = f'/images/user_{telegram_id}.jpg'
            response_data = create_wallet_response.json()
            wallet_address = response_data.get('address')
            customer_data = {
            'username': username,
            'telegram_id': telegram_id,
            'wallet_address':wallet_address,
            # 'image':image_path,
            'balance':0.0,
            'password':password
            }
            # Save the customer data (including the wallet address) to the database
            created_customer = customer_service.create_customer(customer_data)
            return jsonify({'message': 'Customer created successfully', 'customer': created_customer})

    else:
            # If there was an error creating the wallet, return an error response
            return jsonify({'message': 'Error creating wallet for the customer'}), create_wallet_response.status_code

@customer_routes.route('/api/customer/<int:telegram_id>', methods=['GET'])
def get_customer(telegram_id):
    print("get customer id",telegram_id)
    customer = customer_service.get_customer_by_telegram_id(telegram_id)
    print("customer 873045706",customer)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({'message': 'Customer not found'}), 404

@customer_routes.route('/api/customers/<int:telegram_id>', methods=['PUT'])
def update_customer(telegram_id):
    data = request.get_json()
    updated_customer = customer_service.update_customer(telegram_id, data)
    if updated_customer:
        return jsonify({'message': 'Customer updated successfully', 'customer': updated_customer})
    else:
        return jsonify({'message': 'Customer not found'}), 404

@customer_routes.route('/api/customers/<int:telegram_id>', methods=['DELETE'])
def delete_customer(telegram_id):
    result = customer_service.delete_customer(telegram_id)
    if result:
        return jsonify({'message': 'Customer deleted successfully'})
    else:
        return jsonify({'message': 'Customer not found'}), 404

from flask import request, jsonify
@customer_routes.route('/api/authenticate', methods=['POST'])
def authenticate_user():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print("Username",username)

        # Call the authenticate_customer function from the CustomerService class
        authenticated, customer = customer_service.authenticate_customer(username, password)

    if authenticated and customer is not None:
        return jsonify({'message': 'Authentication successful', 'customer': customer})
    else:
        return jsonify({'message': 'Authentication failed. Invalid username or password'}), 401



@customer_routes.route('/api/update_balance/<int:telegram_id>', methods=['POST'])
def update_customer_balance(telegram_id):
    data = request.get_json()
    available_balance = data.get('available_balance')

    if available_balance is not None:
        updated_customer = customer_service.update_customer_balance(telegram_id, available_balance)

        if updated_customer:
            return jsonify({'message': 'Customer balance updated successfully', 'customer': updated_customer})
        else:
            return jsonify({'message': 'Customer not found'}), 404
    else:
        return jsonify({'message': 'Available balance not provided.'}), 400