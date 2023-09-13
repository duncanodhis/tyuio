from flask import Blueprint, jsonify, request
from models.order import Order
from services.order_service import OrderService

order_view = Blueprint('order_view', __name__)
order_service = OrderService()

@order_view.route('/orders', methods=['GET'])
def get_orders():
    orders = order_service.get_orders()
    return jsonify(orders)

@order_view.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    created_order = order_service.create_order(order)
    return jsonify({'message': 'Order created successfully', 'order': created_order})

@order_view.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = order_service.get_order(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_view.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    updated_order = order_service.update_order(order_id, data)
    if updated_order:
        return jsonify({'message': 'Order updated successfully', 'order': updated_order})
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_view.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = order_service.delete_order(order_id)
    if result:
        return jsonify({'message': 'Order deleted successfully'})
    else:
        return jsonify({'message': 'Order not found'}), 404
