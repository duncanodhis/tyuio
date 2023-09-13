from models.payment import Payment,Wallet
from app import db

class PaymentService:
    def get_payments(self):
        payments = Payment.query.all()
        return [self._convert_to_dict(payment) for payment in payments]

    def get_payment(self, payment_id):
        payment = Payment.query.get(payment_id)
        return self._convert_to_dict(payment) if payment else None

    def create_payment(self, data):
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        return self._convert_to_dict(payment)
    
    def create_payment_wallet(self,wallet_address):
        # Check if a wallet record already exists
        existing_wallet = Wallet.query.first()

        if existing_wallet:
            # If a wallet record exists, update its wallet address
            existing_wallet.wallet_address = wallet_address
        else:
            # If no wallet record exists, create a new one
            new_wallet = Wallet(wallet_address=wallet_address)
            db.session.add(new_wallet)

        db.session.commit()
    
    def get_wallet_address(self):
        # Retrieve the wallet address if it exists
        wallet = Wallet.query.first()
        if wallet:
            return wallet.wallet_address
        else:
            return None 

    def update_payment(self, payment_id, data):
        payment = Payment.query.get(payment_id)
        if payment:
            for key, value in data.items():
                setattr(payment, key, value)
            db.session.commit()
            return self._convert_to_dict(payment)
        return None

    def delete_payment(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, payment):
        if payment:
            return {key: getattr(payment, key) for key in payment.__dict__.keys() if not key.startswith('_')}
        return None
