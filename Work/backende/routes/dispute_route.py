from flask import Blueprint, jsonify, request
from models.dispute import Dispute
from services.dispute_service import DisputeService

dispute_routes = Blueprint('dispute_routes', __name__)
dispute_service = DisputeService()

@dispute_routes.route('/api/disputes', methods=['GET'])
def get_disputes():
    disputes = dispute_service.get_dispute_data() 
    return jsonify(disputes)

@dispute_routes.route('/api/disputes', methods=['POST'])
def create_dispute():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    message = data.get('message')
    urgency = data.get('urgency')
    order_id = data.get('order_id')
    data ={
        'user_id':telegram_id,
        'message':message,
        'urgency':urgency,
        'order_id':order_id,
        'status':'pending'
        }

    created_dispute = dispute_service.create_dispute(data)
    return jsonify({'message': 'Dispute created successfully', 'dispute': created_dispute})

@dispute_routes.route('/api/disputes/<int:dispute_id>', methods=['GET'])
def get_dispute(dispute_id):
    dispute = dispute_service.get_dispute(dispute_id)
    if dispute:
        return jsonify(dispute)
    else:
        return jsonify({'message': 'Dispute not found'}), 404

@dispute_routes.route('/api/disputes/<int:dispute_id>/updateStatus', methods=['PUT'])  # Added /updateStatus
def update_dispute_status(dispute_id):
    status = request.form.get('status')
    print("status",status)
    updated_dispute = dispute_service.update_dispute_status(dispute_id, status)  # Use the update_dispute_status method
    if updated_dispute:
        return jsonify({'message': 'Dispute status updated successfully', 'dispute': updated_dispute})
    else:
        return jsonify({'message': 'Dispute not found'}), 404

@dispute_routes.route('/api/disputes/<int:dispute_id>', methods=['DELETE'])
def delete_dispute(dispute_id):
    result = dispute_service.delete_dispute(dispute_id)
    if result:
        return jsonify({'message': 'Dispute deleted successfully'})
    else:
        return jsonify({'message': 'Dispute not found'}), 404
