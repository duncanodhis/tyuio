from models.review import Review
from app import db

class ReviewService:
    def get_reviews(self):
        reviews = Review.query.all()
        return [self._convert_to_dict(review) for review in reviews]

    def get_review(self, review_id):
        review = Review.query.get(review_id)
        return self._convert_to_dict(review) if review else None

    def create_review(self, data):
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return self._convert_to_dict(review)

    def update_review(self, review_id, data):
        review = Review.query.get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
            return self._convert_to_dict(review)
        return None

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False

    def get_reviews_with_details(self):
        reviews = Review.query.join(Review.user, Review.product, Review.order).all()
        return [self._convert_to_dict_with_details(review) for review in reviews]

    def _convert_to_dict_with_details(self, review):
        if review:
            return {
                'Customer ID': review.user.telegram_id,
                'Customer Name': review.user.name,
                'Product ID': review.product.id,
                'Product Name': review.product.name,
                'Rating': review.rating,
                'Comment': review.comment,
                'Order': review.order.order_number if review.order else 'N/A',
                'Created At': review.created_at,
            }
        return None

    def _convert_to_dict(self, review):
        if review:
            return {key: getattr(review, key) for key in review.__dict__.keys() if not key.startswith('_')}
        return None
