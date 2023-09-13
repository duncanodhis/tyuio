from models.customer import Customer
from app import db

class CustomerService:
    def get_customers(self):
        customers = Customer.query.all()
        return [self._convert_to_dict(customer) for customer in customers]

    def get_customer(self, customer_id):
        customer = Customer.query.get(customer_id)
        return self._convert_to_dict(customer) if customer else None
    
    def get_customer_by_telegram_id(self, telegram_id):
        customer = Customer.query.filter_by(telegram_id=telegram_id).first()
        return self._convert_to_dict(customer) if customer else None

    def create_customer(self, data):
        customer = Customer(**data)
        db.session.add(customer)
        db.session.commit()
        return self._convert_to_dict(customer)

    def update_customer(self, customer_id, data):
        customer = Customer.query.get(customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            db.session.commit()
            return self._convert_to_dict(customer)
        return None

    def delete_customer(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return True
        return False
    
    def authenticate_customer(self, username, password):
        customer = Customer.query.filter_by(username=username).first()
        
        # If no customer with the given username is found, authentication fails
        if not customer:
            return False, None

        # Here, you should use a secure password hashing method like bcrypt to compare passwords
        # For this example, we'll use a simple comparison, but in a real-world scenario, use bcrypt or a similar library.
        if customer.password == password:
            # If the passwords match, return True and the customer data
            return True, self._convert_to_dict(customer)

        # If the passwords do not match, authentication fails
        return False, None
    
    def get_customer_data(self):
        # Retrieve data for the table
        customers = Customer.query.all()
        data = []

        for customer in customers:
            total_expenditure = sum([order.total_price for order in customer.orders])
            purchases = len(customer.orders)
            disputes = len(customer.disputes)
            reviews = len(customer.reviews)

            customer_data = {
                'Telegram ID': customer.telegram_id,
                'wallet_address':customer.wallet_address,
                'First Name': customer.username,
                'Last Name': '',  # You can fetch the last name if available
                'Date Joined': customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Balance': customer.balance,
                'All Time Expenditure': total_expenditure,
                'Purchases': purchases,
                'Disputes': disputes,
                'Reviews': reviews,
            }

            data.append(customer_data)

        return data

    def _convert_to_dict(self, customer):
        if customer:
            return {key: getattr(customer, key) for key in customer.__dict__.keys() if not key.startswith('_')}
        return None
   
    def update_customer_balance(telegram_id, available_balance):
        try:
            # Find the customer by telegram_id
            customer = Customer.query.filter_by(telegram_id=telegram_id).first()

            if customer:
                # Update the balance of the customer
                customer.balance = available_balance
                db.session.commit()
                return customer
            else:
                return None
        except Exception as e:
            # Handle exceptions as needed (e.g., logging)
            return None