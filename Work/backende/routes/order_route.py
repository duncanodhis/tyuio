from flask import Blueprint, jsonify, request
from services.order_service import OrderService

order_routes = Blueprint('order_routes', __name__)
order_service = OrderService()

@order_routes.route('/api/orders', methods=['GET'])
def get_orders():
    orders = order_service.get_orders()
    return jsonify(orders)

@order_routes.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    total_price = data.get('total_price')
    number_of_orders = data.get('number_of_orders')
    quantity = data.get('quantity')
    quantity_unit = data.get('quantity_unit')
    product_id = data.get('product_id')
    transaction_id = data.get('transaction_id')
    order_data = {
        'telegram_id': telegram_id,
        'total_price': total_price,
        'number_of_orders': number_of_orders,
        'quantity': quantity,
        'quantity_unit': quantity_unit,
        'product_id': product_id,
        'transaction_id': transaction_id
    }
    
    created_order_id = order_service.create_order(order_data)
    print("created_order",created_order_id)
    associated_treasure_info = order_service.associate_order_with_treasure(created_order_id)
    
    response_data = {
        'message': 'Order created successfully',
        'order': created_order_id,
        'associated_treasure': associated_treasure_info
    }
    
    return jsonify(response_data)

@order_routes.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = order_service.get_order(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_routes.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    updated_order = order_service.update_order(order_id, data)
    if updated_order:
        return jsonify({'message': 'Order updated successfully', 'order': updated_order})
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_routes.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = order_service.delete_order(order_id)
    if result:
        return jsonify({'message': 'Order deleted successfully'})
    else:
        return jsonify({'message': 'Order not found'}), 404

@order_routes.route('/api/orders', methods=['GET'])
def get__orders():
    orders = order_service.get_orders_with_images()
    return jsonify(orders), 200

@order_routes.route('/api/orders/telegram/<string:telegram_id>', methods=['GET'])
def get_orders_by_telegram_id(telegram_id):
    # Call the get_orders_by_telegram_id method to fetch orders for the given Telegram ID
    orders = order_service.get_orders_by_telegram_id(telegram_id)
    
    if orders:
        return jsonify(orders), 200
    else:
        return jsonify({'message': 'No orders found for this Telegram ID'}), 404
