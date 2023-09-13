from flask import Blueprint, jsonify, request
from models.newsletter import Newsletter
from services.newsletter_service import NewsletterService

newsletter_view = Blueprint('newsletter_view', __name__)
newsletter_service = NewsletterService()

@newsletter_view.route('/newsletters', methods=['GET'])
def get_newsletters():
    newsletters = newsletter_service.get_newsletters()
    return jsonify(newsletters)

@newsletter_view.route('/newsletters', methods=['POST'])
def create_newsletter():
    data = request.get_json()
    email = data.get('email')
    subscribed = data.get('subscribed')

    newsletter = Newsletter(email=email, subscribed=subscribed)
    created_newsletter = newsletter_service.create_newsletter(newsletter)
    return jsonify({'message': 'Newsletter created successfully', 'newsletter': created_newsletter})

@newsletter_view.route('/newsletters/<int:newsletter_id>', methods=['GET'])
def get_newsletter(newsletter_id):
    newsletter = newsletter_service.get_newsletter(newsletter_id)
    if newsletter:
        return jsonify(newsletter)
    else:
        return jsonify({'message': 'Newsletter not found'}), 404

@newsletter_view.route('/newsletters/<int:newsletter_id>', methods=['PUT'])
def update_newsletter(newsletter_id):
    data = request.get_json()
    updated_newsletter = newsletter_service.update_newsletter(newsletter_id, data)
    if updated_newsletter:
        return jsonify({'message': 'Newsletter updated successfully', 'newsletter': updated_newsletter})
    else:
        return jsonify({'message': 'Newsletter not found'}), 404

@newsletter_view.route('/newsletters/<int:newsletter_id>', methods=['DELETE'])
def delete_newsletter(newsletter_id):
    result = newsletter_service.delete_newsletter(newsletter_id)
    if result:
        return jsonify({'message': 'Newsletter deleted successfully'})
    else:
        return jsonify({'message': 'Newsletter not found'}), 404
