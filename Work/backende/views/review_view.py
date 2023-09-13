from flask import Blueprint, jsonify, request
from models.review import Review
from services.review_service import ReviewService

review_view = Blueprint('review_view', __name__)
review_service = ReviewService()

@review_view.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = review_service.get_reviews()
    return jsonify(reviews)

@review_view.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment')

    review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
    created_review = review_service.create_review(review)
    return jsonify({'message': 'Review created successfully', 'review': created_review})

@review_view.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = review_service.get_review(review_id)
    if review:
        return jsonify(review)
    else:
        return jsonify({'message': 'Review not found'}), 404

@review_view.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    updated_review = review_service.update_review(review_id, data)
    if updated_review:
        return jsonify({'message': 'Review updated successfully', 'review': updated_review})
    else:
        return jsonify({'message': 'Review not found'}), 404

@review_view.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    result = review_service.delete_review(review_id)
    if result:
        return jsonify({'message': 'Review deleted successfully'})
    else:
        return jsonify({'message': 'Review not found'}), 404
