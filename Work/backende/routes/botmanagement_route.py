from flask import Blueprint,Flask, request, jsonify
from services.botmanagement_service import BotManagementService

botmanagement_route = Blueprint('botmanagement_routes', __name__)

# Create a BotManagementService instance
bot_service = BotManagementService()


# Create Shop Telegram Bot
@botmanagement_route.route('/api/create/shop_bot', methods=['POST'])
def create_shop_bot():
    try:
        data = request.get_json()
        token = data.get('telegramToken')
        # print("token",token)
        if not token:
            return jsonify({'error': 'Token is required'}), 400

        bot = bot_service.create_shop_telegram_bot(token)
        return jsonify({'message': f'Shop Telegram Bot created with ID {bot.id}'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Get Shop Telegram Bot by ID
@botmanagement_route.route('/api/get/shop_bot/<int:bot_id>', methods=['GET'])
def get_shop_bot(bot_id):
    bot = bot_service.get_shop_telegram_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Shop Telegram Bot not found'}), 404
    
    return jsonify({'id': bot.id, 'token': bot.token})

# Update Shop Telegram Bot by ID
@botmanagement_route.route('/api/update/shop_bot/<int:bot_id>', methods=['PUT'])
def update_shop_bot(bot_id):
    data = request.get_json()
    new_token = data.get('new_token')
    
    if not new_token:
        return jsonify({'error': 'New token is required'}), 400
    
    bot = bot_service.update_shop_telegram_bot(bot_id, new_token)
    
    if not bot:
        return jsonify({'error': 'Shop Telegram Bot not found'}), 404
    
    return jsonify({'message': f'Shop Telegram Bot with ID {bot.id} updated'}), 200

# Delete Shop Telegram Bot by ID
@botmanagement_route.route('/api/delete/shop_bot/<int:bot_id>', methods=['DELETE'])
def delete_shop_bot(bot_id):
    bot = bot_service.delete_shop_telegram_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Shop Telegram Bot not found'}), 404
    
    return jsonify({'message': f'Shop Telegram Bot with ID {bot.id} deleted'}), 200

# Create Courier Telegram Bot
@botmanagement_route.route('/api/create/courier_bot', methods=['POST'])
def create_courier_bot():
    data = request.get_json()
    token = data.get('telegramToken')
    
    if not token:
        return jsonify({'error': 'Token is required'}), 400

    bot = bot_service.create_courier_telegram_bot(token)
    return jsonify({'message': f'Courier Telegram Bot created with ID {bot.id}'}), 201

# Get Courier Telegram Bot by ID
@botmanagement_route.route('/api/get/courier_bot/<int:bot_id>', methods=['GET'])
def get_courier_bot(bot_id):
    bot = bot_service.get_courier_telegram_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Courier Telegram Bot not found'}), 404
    
    return jsonify({'id': bot.id, 'token': bot.token})

# Update Courier Telegram Bot by ID
@botmanagement_route.route('/api/update/courier_bot/<int:bot_id>', methods=['PUT'])
def update_courier_bot(bot_id):
    data = request.get_json()
    new_token = data.get('new_token')
    
    if not new_token:
        return jsonify({'error': 'New token is required'}), 400
    
    bot = bot_service.update_courier_telegram_bot(bot_id, new_token)
    
    if not bot:
        return jsonify({'error': 'Courier Telegram Bot not found'}), 404
    
    return jsonify({'message': f'Courier Telegram Bot with ID {bot.id} updated'}), 200

# Delete Courier Telegram Bot by ID
@botmanagement_route.route('/api/delete/courier_bot/<int:bot_id>', methods=['DELETE'])
def delete_courier_bot(bot_id):
    bot = bot_service.delete_courier_telegram_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Courier Telegram Bot not found'}), 404
    
    return jsonify({'message': f'Courier Telegram Bot with ID {bot.id} deleted'}), 200

# Create Disputes Reviews Bot
@botmanagement_route.route('/api/create/disputes_reviews_bot', methods=['POST'])
def create_disputes_reviews_bot():
    data = request.get_json()
    token = data.get('telegramToken')
    
    if not token:
        return jsonify({'error': 'Token is required'}), 400

    bot = bot_service.create_disputes_reviews_bot(token)
    return jsonify({'message': f'Disputes Reviews Bot created with ID {bot.id}'}), 201

# Get Disputes Reviews Bot by ID
@botmanagement_route.route('/api/get/disputes_reviews_bot/<int:bot_id>', methods=['GET'])
def get_disputes_reviews_bot(bot_id):
    bot = bot_service.get_disputes_reviews_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Disputes Reviews Bot not found'}), 404
    
    return jsonify({'id': bot.id, 'token': bot.token})

# Update Disputes Reviews Bot by ID
@botmanagement_route.route('/api/update/disputes_reviews_bot/<int:bot_id>', methods=['PUT'])
def update_disputes_reviews_bot(bot_id):
    data = request.get_json()
    new_token = data.get('new_token')
    
    if not new_token:
        return jsonify({'error': 'New token is required'}), 400
    
    bot = bot_service.update_disputes_reviews_bot(bot_id, new_token)
    
    if not bot:
        return jsonify({'error': 'Disputes Reviews Bot not found'}), 404
    
    return jsonify({'message': f'Disputes Reviews Bot with ID {bot.id} updated'}), 200

# Delete Disputes Reviews Bot by ID
@botmanagement_route.route('/api/delete/disputes_reviews_bot/<int:bot_id>', methods=['DELETE'])
def delete_disputes_reviews_bot(bot_id):
    bot = bot_service.delete_disputes_reviews_bot(bot_id)
    
    if not bot:
        return jsonify({'error': 'Disputes Reviews Bot not found'}), 404
    
    return jsonify({'message': f'Disputes Reviews Bot with ID {bot.id} deleted'}), 200

# Create Newsletter Channel
@botmanagement_route.route('/api/create/newsletter_channel', methods=['POST'])
def create_newsletter_channel():
    data = request.get_json()
    channel_id = data.get('channelId')
    token = data.get('telegramToken')
   
    if not channel_id or not token:
        return jsonify({'error': 'Channel ID and Token are required'}), 400

    channel = bot_service.create_newsletter_channel(channel_id, token)
    return jsonify({'message': f'Newsletter Channel created with ID {channel.id}'}), 201

# Get Newsletter Channel by ID
@botmanagement_route.route('/api/get/newsletter_channel/<int:channel_id>', methods=['GET'])
def get_newsletter_channel(channel_id):
    channel = bot_service.get_newsletter_channel(channel_id)
    
    if not channel:
        return jsonify({'error': 'Newsletter Channel not found'}), 404
    
    return jsonify({'id': channel.id, 'channel_id': channel.channel_id, 'token': channel.token})

# Update Newsletter Channel by ID
@botmanagement_route.route('/api/update/newsletter_channel/<int:channel_id>', methods=['PUT'])
def update_newsletter_channel(channel_id):
    data = request.get_json()
    new_token = data.get('new_token')
    
    if not new_token:
        return jsonify({'error': 'New token is required'}), 400
    
    channel = bot_service.update_newsletter_channel(channel_id, new_token)
    
    if not channel:
        return jsonify({'error': 'Newsletter Channel not found'}), 404
    
    return jsonify({'message': f'Newsletter Channel with ID {channel.id} updated'}), 200

# Delete Newsletter Channel by ID
@botmanagement_route.route('/api/delete/newsletter_channel/<int:channel_id>', methods=['DELETE'])
def delete_newsletter_channel(channel_id):
    channel = bot_service.delete_newsletter_channel(channel_id)
    
    if not channel:
        return jsonify({'error': 'Newsletter Channel not found'}), 404
    
    return jsonify({'message': f'Newsletter Channel with ID {channel.id} deleted'}), 200

@botmanagement_route.route('/api/latest/shop_bot', methods=['GET'])
def get_latest_shop_bot_token():
    latest_shop_bot = bot_service.get_latest_shop_telegram_bot()
    if latest_shop_bot:
        return jsonify({'token': latest_shop_bot.token}), 200
    else:
        return jsonify({'error': 'No Shop Telegram Bot found'}), 404

@botmanagement_route.route('/api/latest/courier_bot', methods=['GET'])
def get_latest_courier_bot_token():
    latest_courier_bot = bot_service.get_latest_courier_telegram_bot()
    if latest_courier_bot:
        return jsonify({'token': latest_courier_bot.token}), 200
    else:
        return jsonify({'error': 'No Courier Telegram Bot found'}), 404

# Route to get the latest Disputes Reviews Bot token
@botmanagement_route.route('/api/latest/disputes_reviews_bot', methods=['GET'])
def get_latest_disputes_reviews_bot_token():
    latest_disputes_reviews_bot = bot_service.get_latest_disputes_reviews_bot()
    if latest_disputes_reviews_bot:
        return jsonify({'token': latest_disputes_reviews_bot.token}), 200
    else:
        return jsonify({'error': 'No Disputes Reviews Bot found'}), 404

# Route to get the latest Newsletter Channel token
@botmanagement_route.route('/api/latest/newsletter_channel', methods=['GET'])
def get_latest_newsletter_channel_token():
    latest_newsletter_channel = bot_service.get_latest_newsletter_channel()
    if latest_newsletter_channel:
        return jsonify({'token': latest_newsletter_channel.token}), 200
    else:
        return jsonify({'error': 'No Newsletter Channel found'}), 404

