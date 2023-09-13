from flask import Blueprint, jsonify, request
from services.task_service import TaskService
from services.product_service import ProductService
task_routes = Blueprint('task_routes', __name__)
task_service = TaskService()
product_service = ProductService()

@task_routes.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = task_service.get_tasks()
    return jsonify(tasks)

@task_routes.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_name= data.get('taskName')
    number_of_treasures = data.get('number_of_treasures')
    # print("No. of treasures",number_of_treasures)
    area_of_distribution = data.get('address')
    commission = data.get('courier_commission')
    commission_currency = data.get('commission_currency')
    cost_of_item = data.get('cost_of_item')
    weight_of_item = data.get('weight_of_item')
    item_weight_measurement = data.get('item_weight_measurement')
    number_of_items = data.get('number_of_items')
    status = "Pending"  # Default status is set to "Pending"
    courier_id = data.get('courier')
    product_id = data.get('product')
    product = product_service.get_product(product_id)
    data = {
        'name':task_name,
        'number_of_treasures':number_of_treasures,
        'courier_id':courier_id,
        'address':product['city'],
        'product_id':product_id,
        'area_of_distribution' : area_of_distribution,
        'number_of_items' : number_of_items,
        'cost_of_item' : cost_of_item,
        'weight_of_item': weight_of_item,
        'item_weight_measurement':  item_weight_measurement,
        'commission': commission,
        'commission_currency' : commission_currency,
        'status':status,
    }
    created_task = task_service.create_task(data)
    return jsonify({'message': 'Task created successfully', 'task': created_task}), 201

@task_routes.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = task_service.get_task(task_id)
    if task:
        return jsonify(task)
    else:
        return jsonify({'message': 'Task not found'}), 404

@task_routes.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    updated_task = task_service.update_task(task_id, data)
    if updated_task:
        return jsonify({'message': 'Task updated successfully', 'task': updated_task})
    else:
        return jsonify({'message': 'Task not found'}), 404

@task_routes.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = task_service.delete_task(task_id)
    if result:
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'}), 404

@task_routes.route('/api/couriers/<int:courier_id>/tasks', methods=['GET'])
def get_tasks_for_courier(courier_id):
    tasks = task_service.get_tasks_for_courier(courier_id)
    return jsonify(tasks)

@task_routes.route('/api/couriers/<int:courier_id>/tasks/<int:task_id>', methods=['GET'])
def get_task_for_courier(courier_id, task_id):
    task = task_service.get_task(task_id)  # You might want to modify this to only fetch tasks for the specific courier
    if task and task['courier_id'] == courier_id:
        return jsonify(task)
    return jsonify({'message': 'Task not found for the specified courier'}), 404

@task_routes.route('/api/couriers/<int:courier_id>/pending-tasks', methods=['GET'])
def get_pending_tasks_for_courier_route(courier_id):
    pending_tasks = task_service.get_pending_and_incomplete_tasks_for_courier(courier_id)
    return jsonify(pending_tasks)