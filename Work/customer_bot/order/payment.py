from flask import Blueprint
from app.models.models import Customer, Order
from app import db
from block_io import BlockIo
from decimal import Decimal
import json
import block_io
import qrcode
import os
import qrcode
import uuid


payment_controller = Blueprint("payment_controller", __name__, template_folder='templates', static_folder='static')

os.environ['CRYPTO_KEY'] = '9744-0ae1-a928-95fb'
os.environ['CRYPTO_CHAIN'] = 'keepyourmouth404'
version = 2

print(os.environ.get('CRYPTO_KEY'), os.environ.get('CRYPTO_CHAIN'))

crypto_block = BlockIo(os.environ.get('CRYPTO_KEY'), os.environ.get('CRYPTO_CHAIN'), version)

def create_customer_wallet(telegram_id, username):
    try:
        wallet_name = str(telegram_id)

        # Check if the wallet address already exists
        existing_address = crypto_block.get_address_by_label(label='user' + wallet_name)
        print("exisiting  wallet ",existing_address)
        if 'data' in existing_address and 'address' in existing_address['data']:
            address_string = existing_address['data']['address']
        else:
            # Create a new wallet address
            new_address = crypto_block.get_new_address(label='user' + wallet_name)
            address_string = new_address['data']['address']
            print(address_string)

        # Check if the wallet address already exists in the database
        customer = Customer.query.filter_by(wallet_address=address_string).first()
        if customer:
            # Update the customer's details only if they have a different telegram_id or username
            if customer.telegram_id != telegram_id or customer.username != username:
                customer.telegram_id = telegram_id
                customer.username = username
                customer.wallet_address = address_string
        else:
            # Create a new customer entry
            new_customer = Customer(telegram_id=telegram_id, username=username, wallet_address=address_string)
            # customer.telegram_id = telegram_id
            # customer.username = username
            # customer.wallet_address = address_string
            db.session.add(new_customer)

        db.session.commit()
        print("Wallet address: " + address_string)
        return address_string  # Return the wallet address

    except Exception as e:
        print(e)
        db.session.rollback()  # Rollback changes in case of an error
        raise Exception('Error creating wallet')

def get_customer_wallet_balance(user_id, app):
    with app.app_context():
        # Check the customer's Litecoin wallet balance using the BlockIo API
        wallet_address = get_customer_wallet_address(user_id, app)
        if not wallet_address:
            raise Exception('Error retrieving wallet address')

        try:
            response = crypto_block.get_address_balance(address=wallet_address)
            available_balance = Decimal(response['data']['available_balance'])
            network = response['data']['network']

            print("New Balance for =", str(user_id) + ":", format(available_balance, '.8f'), network)
            balance = format(available_balance, '.8f')
            customer = Customer.query.filter_by(telegram_id=user_id).first()
            if customer:
                customer.wallet_balance = balance
                db.session.commit()

            return balance

        except Exception as e:
            print(e)
            raise Exception('Error retrieving wallet balance')

def create_payment_request(user_id, order_id, app):
    # Create a payment request for an order using the BlockIo API
    # Store the payment address and transaction ID in the Order model
    with app.app_context():
        order = Order.query.get(order_id)
        if not order:
            raise Exception('Order not found')

        amount_to_send = order.amount
        customer_address = get_customer_wallet_address(user_id, app)
        merchant_address = order.merchant_address
        print("Sending Coins =", format(amount_to_send, '.8f'), "to Label =", merchant_address)

        try:
            prepared_transaction = crypto_block.prepare_transaction(
                amount=format(amount_to_send, '.8f'),
                from_addresses=customer_address,
                to_addresses=merchant_address
            )

            print("Transaction and network fees required =", json.dumps(crypto_block.summarize_prepared_transaction(prepared_transaction)))

            created_transaction_and_signatures = crypto_block.create_and_sign_transaction(prepared_transaction)

            response = crypto_block.submit_transaction(transaction_data=created_transaction_and_signatures)

            if response and 'data' in response:
                print("checking transaction response"+str(response))
                order.payment_address = response['data']['txid']
                order.txn_id = response['data']['txid']
                order.payment_status = "paid"
                db.session.commit()
            else:
                raise Exception('Error creating payment request')
        except Exception as e:
            print(e)
            raise Exception('Error creating payment request')

def topup_customer_wallet(customer_id, amount):
    # Get the customer's Litecoin wallet address
    customer = Customer.query.get(customer_id)
    if not customer:
        raise Exception("Customer not found")
    wallet_address = customer.wallet_address

    return wallet_address

def process_topup(telegram_id, amount, app):
    # Create a payment request for the top-up using the BlockIo API
    with app.app_context():
        customer = Customer.query.filter_by(telegram_id=telegram_id).first()
        if not customer:
            raise Exception('Customer not found')
        payment_address = str(customer.wallet_address)  # Convert to string
        # Generate a unique filename for the QR code image
        unique_filename = payment_address + '_' + str(uuid.uuid4()) + '.png'
        qr_code_path = os.path.join('img', 'qrcodeImages', unique_filename)

        # Generate a QR code for the payment address
        qr_code = qrcode.make(payment_address)
        qr_code_url = qr_code_path
        qr_code.save(qr_code_url)

        # Return the payment address and QR code URL
        return payment_address, qr_code_url

def confirm_payment(txn_id,app):
    # Check the status of a payment using the BlockIo API
    # Update the order status based on the payment status
    with app.app_context():
        order = Order.query.filter_by(txn_id=txn_id).first()
        if not order:
            raise Exception('Order not found')

    
        response = crypto_block.get_transaction_details(txid=txn_id)

        if response and 'data' in response:
            confirmations = response['data']['confirmations']
            if confirmations >= 6:
                print('Payment is complete')
                order.payment_status = 'Paid'
                db.session.commit()
                return True
            else:
                print('Payment is still pending')
                return False
        else:
            raise Exception('Error checking payment status')

def confirm_payment_of_order(order_id, coin_symbol='ltc'):
    # Check the status of a payment using the BlockIo API
    # Update the order status based on the payment status
    order = Order.query.get(order_id)
    if not order:
        raise Exception('Order not found')

    response = crypto_block.get_transaction_info(txid=order.txn_id, coin_symbol=coin_symbol)

    if response and 'data' in response:
        confirmations = response['data']['confirmations']
        if confirmations > 0:
            order.payment_status = 'Paid'
        else:
            order.payment_status = 'Pending'
        db.session.commit()
    else:
        raise Exception('Error checking payment status')

def handle_start_button(telegram_id, username, app):
    with app.app_context():
        # Check if the user exists, and create a new user if needed
        user = Customer.query.filter_by(telegram_id=telegram_id).first()
        print("getting user id in handle start button",user)
        if not user:
            user = Customer(telegram_id=telegram_id, username=username,
                            wallet_address = create_customer_wallet(telegram_id=telegram_id, 
                                                                    username=username))
            db.session.add(user)
            db.session.commit()

        # Check if the customer exists, and create a new customer with a wallet if needed
        customer = Customer.query.filter_by(telegram_id=telegram_id).first()
        if not customer:
            try:
                wallet_address = create_customer_wallet(telegram_id=telegram_id, username=username)
                customer = Customer(telegram_id=telegram_id, username=username, wallet_address=wallet_address)
                db.session.add(customer)
                db.session.commit()
            except Exception as e:
                print(e)
                raise Exception('Error creating customer with wallet address')

def get_customer_wallet_address(user_id, app):
    with app.app_context():
        customer = Customer.query.filter_by(telegram_id=user_id).first()
        if not customer:
            raise Exception('Customer not found')

        return customer.wallet_address


#skull scare awesome able battle garlic curious true chimney insane bulb end