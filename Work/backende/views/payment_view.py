from flask import Blueprint, jsonify, request
from models.payment import Payment
from services.payment_service import PaymentService

payment_view = Blueprint('payment_view', __name__)
payment_service = PaymentService()

@payment_view.route('/payments', methods=['GET'])
def get_payments():
    payments = payment_service.get_payments()
    return jsonify(payments)

@payment_view.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    amount = data.get('amount')
    currency = data.get('currency')
    status = data.get('status')

    payment = Payment(order_id=order_id, amount=amount, currency=currency, status=status)
    created_payment = payment_service.create_payment(payment)
    return jsonify({'message': 'Payment created successfully', 'payment': created_payment})

@payment_view.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = payment_service.get_payment(payment_id)
    if payment:
        return jsonify(payment)
    else:
        return jsonify({'message': 'Payment not found'}), 404

@payment_view.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.get_json()
    updated_payment = payment_service.update_payment(payment_id, data)
    if updated_payment:
        return jsonify({'message': 'Payment updated successfully', 'payment': updated_payment})
    else:
        return jsonify({'message': 'Payment not found'}), 404

@payment_view.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    result = payment_service.delete_payment(payment_id)
    if result:
        return jsonify({'message': 'Payment deleted successfully'})
    else:
        return jsonify({'message': 'Payment not found'}), 404
