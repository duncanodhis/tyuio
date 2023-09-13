from models.dispute import Dispute
from app import db

class DisputeService:
    def get_disputes(self):
        disputes = Dispute.query.all()
        return [self._convert_to_dict(dispute) for dispute in disputes]

    def get_dispute(self, dispute_id):
        dispute = Dispute.query.get(dispute_id)
        return self._convert_to_dict(dispute) if dispute else None

    def create_dispute(self, data):
        dispute = Dispute(**data)
        db.session.add(dispute)
        db.session.commit()
        return self._convert_to_dict(dispute)

    def update_dispute(self, dispute_id, data):
        dispute = Dispute.query.get(dispute_id)
        if dispute:
            for key, value in data.items():
                setattr(dispute, key, value)
            db.session.commit()
            return self._convert_to_dict(dispute)
        return None

    def delete_dispute(self, dispute_id):
        dispute = Dispute.query.get(dispute_id)
        if dispute:
            db.session.delete(dispute)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, dispute):
        if dispute:
            return {key: getattr(dispute, key) for key in dispute.__dict__.keys() if not key.startswith('_')}
        return None

    def update_dispute_status(self, dispute_id, status):
        dispute = Dispute.query.get(dispute_id)
        if dispute:
            dispute.status = status
            db.session.commit()
            return self._convert_to_dict(dispute)
        return None
 
    def get_dispute_data(self):
        disputes = Dispute.query.all()
        dispute_data = []

        for dispute in disputes:
            dispute_dict = {
                'order_id': dispute.order_id,
                'user_id': dispute.user_id,
                'product_name': dispute.order.product.name,
                'message': dispute.message,
                'status': dispute.status,
                'created_at': dispute.created_at,
                # You can add more fields if needed for actions
            }
            dispute_data.append(dispute_dict)

        return dispute_data
