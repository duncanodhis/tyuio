from flask import Blueprint, jsonify, request
from models.dispute import Dispute
from services.dispute_service import DisputeService

dispute_view = Blueprint('dispute_view', __name__)
dispute_service = DisputeService()

@dispute_view.route('/disputes', methods=['GET'])
def get_disputes():
    disputes = dispute_service.get_disputes()
    return jsonify(disputes)

@dispute_view.route('/disputes', methods=['POST'])
def create_dispute():
    data = request.get_json()
    order_id = data.get('order_id')
    reason = data.get('reason')
    description = data.get('description')

    dispute = Dispute(order_id=order_id, reason=reason, description=description)
    created_dispute = dispute_service.create_dispute(dispute)
    return jsonify({'message': 'Dispute created successfully', 'dispute': created_dispute})

@dispute_view.route('/disputes/<int:dispute_id>', methods=['GET'])
def get_dispute(dispute_id):
    dispute = dispute_service.get_dispute(dispute_id)
    if dispute:
        return jsonify(dispute)
    else:
        return jsonify({'message': 'Dispute not found'}), 404

@dispute_view.route('/disputes/<int:dispute_id>', methods=['PUT'])
def update_dispute(dispute_id):
    data = request.get_json()
    updated_dispute = dispute_service.update_dispute(dispute_id, data)
    if updated_dispute:
        return jsonify({'message': 'Dispute updated successfully', 'dispute': updated_dispute})
    else:
        return jsonify({'message': 'Dispute not found'}), 404

@dispute_view.route('/disputes/<int:dispute_id>', methods=['DELETE'])
def delete_dispute(dispute_id):
    result = dispute_service.delete_dispute(dispute_id)
    if result:
        return jsonify({'message': 'Dispute deleted successfully'})
    else:
        return jsonify({'message': 'Dispute not found'}), 404
