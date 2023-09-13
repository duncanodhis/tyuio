from flask import Blueprint, jsonify, request
from services.courier_service import CourierService

courier_routes = Blueprint('courier_routes', __name__)
courier_service = CourierService()

@courier_routes.route('/api/couriers', methods=['GET'])
def get_couriers():
    couriers = courier_service.get_couriers()
    return jsonify(couriers)

@courier_routes.route('/api/couriers', methods=['POST'])
def create_courier():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  
    #Code to create the product_data dictionary
    data = {
        'name':username,
        'password':password
    }
    created_courier = courier_service.create_courier(data)
    return jsonify({'message': 'Courier created successfully', 'courier': created_courier}), 201

@courier_routes.route('/api/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = courier_service.get_courier(courier_id)
    if courier:
        return jsonify(courier)
    else:
        return jsonify({'message': 'Courier not found'}), 404

@courier_routes.route('/api/couriers/<int:courier_id>', methods=['PUT'])
def update_courier(courier_id):
    data = request.get_json()
    updated_courier = courier_service.update_courier(courier_id, data)
    if updated_courier:
        return jsonify({'message': 'Courier updated successfully', 'courier': updated_courier})
    else:
        return jsonify({'message': 'Courier not found'}), 404

@courier_routes.route('/api/couriers/<int:courier_id>', methods=['DELETE'])
def delete_courier(courier_id):
    result = courier_service.delete_courier(courier_id)
    if result:
        return jsonify({'message': 'Courier deleted successfully'})
    else:
        return jsonify({'message': 'Courier not found'}), 404

@courier_routes.route('/api/couriers_with_tasks', methods=['GET'])
def get_couriers_with_tasks():
    couriers = courier_service.get_couriers_with_tasks()
    print(couriers)
    return jsonify(couriers)

@courier_routes.route('/api/couriers/<int:courier_id>/tasks', methods=['GET'])
def get_courier_tasks(courier_id):
    tasks = courier_service.get_courier_tasks(courier_id)
    if tasks:
        return jsonify(tasks), 200
    else:
        return jsonify({'message': 'Courier not found'}), 404

# Fetch a specific task for a courier
@courier_routes.route('/api/couriers/<int:courier_id>/tasks/<int:task_id>', methods=['GET'])
def get_courier_task(courier_id, task_id):
    task = courier_service.get_courier_task(courier_id, task_id)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({'message': 'Task not found'}), 404
@courier_routes.route('/api/authenticate', methods=['POST'])

def authenticate_courier():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    courier = courier_service.authenticate_courier(username, password)
    if courier:
        return jsonify({'message': 'Authentication successful', 'courier': courier}), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401
    
@courier_routes.route('/api/couriers/<int:courier_id>/earnings', methods=['GET'])
def get_courier_earning(courier_id):
    updated_earning = courier_service.update_courier_total_earning(courier_id)
    if updated_earning is not None:
        return jsonify({'earning': updated_earning}), 200
    else:
        return jsonify({'message': 'Courier not found'}), 404
