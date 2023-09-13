from flask import Blueprint, jsonify, request
from models.payment import Payment
from services.payment_service import PaymentService
from flask import Flask, request, jsonify
from block_io import BlockIo
import uuid
import json
import requests

payment_routes = Blueprint('payment_routes', __name__)
payment_service = PaymentService()
# This should be replaced with your own Blockio API token
version = 2 # API version
block_io = BlockIo('9c46-581f-5438-412f', 'Summer2023BreezeBeach', version)

@payment_routes.route('/api/create_wallet', methods=['POST'])
def create_wallet():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    # print("c t",telegram_id)
    if telegram_id:
        # Check if the user already has an address
        existing_address = check_user_address(telegram_id)
        if existing_address:
            return jsonify({'address': existing_address, 'message': 'User already has an address.'})
        else:
            # Create a new address with the Telegram ID as the label
            new_address = create_or_get_user_address(telegram_id)
            payment_service.create_payment(new_address)
            return jsonify({'address': new_address, 'message': 'New address created.'})
    else:
        return jsonify({'message': 'Telegram ID not provided.'}), 400

@payment_routes.route('/api/get_balance', methods=['GET'])
def get_balance():
    data = request.get_json()
    telegram_id = data.get('telegram_id')

    if telegram_id:
        user_address = check_user_address(telegram_id)
        if user_address is None:
            user_address = create_or_get_user_address(telegram_id)
        balance = block_io.get_address_balance(addresses=user_address)
        print("Available balance",balance)
        available_balance = balance['data']['available_balance']
        # print("THE REAL BALANCE",available_balance)
        return jsonify({'address': user_address, 'available_balance': available_balance})
    else:
        return jsonify({'message': 'Telegram ID not provided.'}), 400   


@payment_routes.route('/api/replenish_wallet', methods=['POST'])
def replenish_wallet():
    data = request.get_json()
    recipient_address = data.get('address')
    amount_in_euro = data.get('amount')
    print("Add", recipient_address)
    print("Amount in Euro", amount_in_euro)
    try:
        # Convert the amount from Euro to BTC
        # btc_amount= convert_to_btc(amount_in_euro)

        # Format the BTC amount to 8 decimal places
        formatted_btc_amount = format(amount_in_euro * 0.000031, '.8f')
        print(f"BTC Amount: {formatted_btc_amount}")

        # Prepare the transaction
        prepared_transaction = block_io.prepare_transaction(to_addresses=recipient_address, amounts=formatted_btc_amount)

        # Review the prepared transaction data
        print(json.dumps(block_io.summarize_prepared_transaction(prepared_transaction)))

        # Create and sign the transaction
        created_transaction_and_signatures = block_io.create_and_sign_transaction(prepared_transaction)

        # Submit the transaction to Block.io for signature and broadcast
        response = block_io.submit_transaction(transaction_data=created_transaction_and_signatures)

        if response['status'] == 'success':
            transaction_id = response['data']['txid']
            print(f"Coins sent. Transaction ID: {transaction_id}")
            return transaction_id
        else:
            raise Exception(response['data']['error_message'])
    except Exception as e:
        raise Exception(f'Error replenishing wallet: {str(e)}')

def send_transaction(recipient_address, amount_in_euro):
    try:
        # Convert the amount from Euro to BTC
        # btc_amount = convert_to_btc(amount_in_euro)
        # print("send_transaction",btc_amount)
        # Prepare the transaction data
        prepare_response = block_io.prepare_transaction(amounts=amount_in_euro*1, to_addresses=recipient_address)
        print(prepare_response)
        # Create and sign the transaction
        transaction_data = block_io.create_and_sign_transaction(prepare_response)

        # Submit the transaction
        submit_response = block_io.submit_transaction(transaction_data=transaction_data)

        if submit_response['status'] == 'success':
            return submit_response['data']['txid']
        else:
            raise Exception(submit_response['data']['error_message'])
    except Exception as e:
        raise Exception(f'Error sending transaction: {str(e)}')

def payment(amount_,amount_currency,from__address,to__address):
    
    try:
        # Convert the amount from Euro to BTC
        to_currency = 'BTC'
        btc_amount = get_currency_conversion(amount_currency, to_currency, amount_)
        print("type of amount",type(btc_amount),btc_amount)
        # print("send_transaction",btc_amount)
        # Prepare the transaction data
        prepare_response = block_io.prepare_transaction(amounts=str(btc_amount), from_addresses=from__address, to_addresses=to__address)
        # Create and sign the transaction
        transaction_data = block_io.create_and_sign_transaction(prepare_response)

        # Submit the transaction
        submit_response = block_io.submit_transaction(transaction_data=transaction_data)

        if submit_response['status'] == 'success':
            return submit_response['data']['txid']
        else:
            raise Exception(submit_response['data']['error_message'])
    except Exception as e:
        raise Exception(f'Error sending transaction: {str(e)}')

@payment_routes.route('/api/make_payment', methods=['POST'])
def make_payment():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    product_currency = data.get('currency')
    from_address = check_user_address(telegram_id)
    recipient_address = payment_service.get_wallet_address()
    amount = data.get('amount')
    if from_address and recipient_address and amount:
        transaction_id = payment(amount,product_currency,from_address, recipient_address)
        
        return jsonify({'transaction_id': transaction_id, 'message': 'Payment successful.'})
    else:
        return jsonify({'message': 'Sender address, recipient address, or amount not provided.'}), 400

def check_user_address(telegram_id):
    # Get all existing addresses from Block.io
    addresses = block_io.get_my_addresses()
    telegram_id_str = str(telegram_id)
    # Search for the user's Telegram ID as the label in the existing addresses
    for address in addresses['data']['addresses']:
        if address['label'] == telegram_id_str:
            return address['address']
# Add 2N5UrhJJuLJcvRW8jynDDqMdapryC2ePPvc
    return None

def create_or_get_user_address(telegram_id):
    # Check if the user already has an address
    existing_address = check_user_address(telegram_id)

    if existing_address:
        # If the user exists, return the existing address
        return existing_address
    else:
        # If the user does not exist, create a new address with the Telegram ID as the label
        telegram_id_str = str(telegram_id)
        new_address_data = block_io.get_new_address(label=telegram_id_str)
        new_address = new_address_data['data']['address']
        return new_address

def get_currency_conversion(from_currency, to_currency, amount):

    api_key = "716e9473c7f083a6e1e4fb97379dfb19"
    base_url = "http://data.fixer.io/api/latest"

    # First, convert from_currency to EUR
    params = {
        "access_key": api_key,
        "base": "EUR",  # Set the base currency to EUR
        "symbols": from_currency
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if "error" in data:
            return f"API Error: {data['error']}"

        exchange_rate = data["rates"][from_currency]
        
        # Now, convert EUR to to_currency
        params = {
            "access_key": api_key,
            "base": "EUR",  # Set the base currency to EUR
            "symbols": to_currency
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if "error" in data:
            return f"API Error: {data['error']}"

        exchange_rate_to = data["rates"][to_currency]
        
        # Calculate the final converted value
        converted_value = (amount / exchange_rate) * exchange_rate_to

        return "{:.5f}".format(converted_value)

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"

@payment_routes.route('/api/create_payment_wallet', methods=['POST'])
def create_payment_wallet():
    try:
        data = request.get_json()
        wallet_address = data.get('walletAddress')  # Make sure the key matches the one sent from the frontend
        # print("Wallet address:", wallet_address)
        payment_service.create_payment_wallet(wallet_address)
        return jsonify({'message': 'Wallet address created successfully'}), 201
    except Exception as e:
        print("error",e)
        return jsonify({'error': str(e)}), 500

@payment_routes.route('/api/get_user_wallet_address', methods=['GET'])
def get_wallet_address():
    wallet_address =  payment_service.get_wallet_address()
    if wallet_address:
        return jsonify({'wallet_address': wallet_address}), 200
    else:
        return jsonify({'message': 'No wallet address found'}), 404