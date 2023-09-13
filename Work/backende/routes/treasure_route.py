
from flask import Blueprint, jsonify, request, current_app, send_file
from models.courier import Treasure  # Import the Treasure model
from services.treasure_service import TreasureService  # Import the TreasureService
from services.task_service import TaskService 
import os

treasure_routes = Blueprint('treasure_routes', __name__)
treasure_service = TreasureService()
task_service = TaskService()


@treasure_routes.route('/api/treasures', methods=['POST'])
def create_treasure():
    data = request.get_json()  # Get JSON data from the request
    # Extract data from the JSON
    task_id = data.get('task_id')
    solution_number = data.get('solution_number')
    description = data.get('description')
    coordinates = data.get('coordinates')
    image_url = data.get('image_url')
    data = {
        'task_id':  task_id,
        'description':description,
        'image_url' :image_url,
        'coordinates': coordinates,
        'status':'retrieved',
        'taken':False
        }
 
    task_service.update_task_treasures_and_status(task_id, solution_number)
    # Save the new Treasure object to the database
    created_treasure = treasure_service.create_treasure(data)
    # print(created_treasure)
    return jsonify({'message': 'Treasure created successfully', 'treasure': created_treasure}), 201
    
@treasure_routes.route('/api/treasures/<int:treasure_id>', methods=['PUT'])
def update_treasure(treasure_id):
    data = request.get_json()
    updated_treasure = treasure_service.update_treasure(treasure_id, data)
    if updated_treasure:
        return jsonify({'message': 'Treasure updated successfully', 'treasure': updated_treasure})
    else:
        return jsonify({'message': 'Treasure not found'}), 404

@treasure_routes.route('/api/treasures/<int:treasure_id>', methods=['DELETE'])
def delete_treasure(treasure_id):
    result = treasure_service.delete_treasure(treasure_id)
    if result:
        return jsonify({'message': 'Treasure deleted successfully'})
    else:
        return jsonify({'message': 'Treasure not found'}), 404
