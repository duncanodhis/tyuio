from flask import Blueprint, jsonify, request
from models.customer import Customer
from services.customer_service import CustomerService

customer_view = Blueprint('customer_view', __name__)
customer_service = CustomerService()

# @customer_view.route('/customers', methods=['GET'])
# def get_customers():
#     customers = customer_service.get_customers()
#     return jsonify(customers)

# @customer_view.route('/customers', methods=['POST'])
# def create_customer():
#     data = request.get_json()
#     username = data.get('username')
#     telegram_id = data.get('telegram_id')
#     balance = data.get('balance')
#     wallet_address = data.get('wallet_address')

#     customer_data = {
#         'username': username,
#         'telegram_id': telegram_id,
#         'balance': balance,
#         'wallet_address': wallet_address
#     }

#     customer = customer_service.create_customer(customer_data)
#     return jsonify({'message': 'Customer created successfully', 'customer': customer})

# @customer_view.route('/customers/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = customer_service.get_customer(customer_id)
#     if customer:
#         return jsonify(customer)
#     else:
#         return jsonify({'message': 'Customer not found'}), 404

# @customer_view.route('/customers/<int:customer_id>', methods=['PUT'])
# def update_customer(customer_id):
#     data = request.get_json()
#     updated_customer = customer_service.update_customer(customer_id, data)
#     if updated_customer:
#         return jsonify({'message': 'Customer updated successfully', 'customer': updated_customer})
#     else:
#         return jsonify({'message': 'Customer not found'}), 404

# @customer_view.route('/customers/<int:customer_id>', methods=['DELETE'])
# def delete_customer(customer_id):
#     result = customer_service.delete_customer(customer_id)
#     if result:
#         return jsonify({'message': 'Customer deleted successfully'})
#     else:
#         return jsonify({'message': 'Customer not found'}), 404
