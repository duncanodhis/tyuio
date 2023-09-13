from flask import Blueprint, jsonify, request,current_app
from models.newsletter import Newsletter
from services.newsletter_service import NewsletterService
from werkzeug.utils import secure_filename 
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import telegram

newsletter_routes = Blueprint('newsletter_routes', __name__)
newsletter_service = NewsletterService()

@newsletter_routes.route('/api/newsletters', methods=['GET'])
def get_newsletters():
    newsletters = newsletter_service.get_newsletters()
    print(newsletters)
    return jsonify(newsletters)

@newsletter_routes.route('/api/newsletters', methods=['POST'])
def create_newsletter():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    message = request.form.get('message')
    file = request.files.get('file')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    # Handle the file upload if it exists
    filename = None  # Initialize filename as None
    if file:
        # Securely save the file with a unique name
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))  # Save the file to the UPLOAD_FOLDER

    data = {
        'message': message,
        'file': filename,
    }

    try:
        # Ensure the UPLOAD_FOLDER exists, create it if not
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # For demonstration purposes, we'll print the uploaded file's path
        if filename is not None:
            print("File saved in:", os.path.join(upload_folder, filename))

        # The rest of your code for creating the newsletter

        created_newsletter = newsletter_service.create_newsletter(data)

        # Send the message and image to the Telegram channel if filename is not None
        # if filename is not None:
        send_message_to_telegram(message, filename)

        return jsonify({'message': 'Newsletter created successfully', 'newsletter': created_newsletter}), 201
    except Exception as e:
        print("error e", e)
        return jsonify({'error': str(e)}), 500

def send_message_to_telegram(message_text, image_filename):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '6188335690:AAHNfwsMaAj6U0P8BHAH69KRfonCCQc_y1I'
    channel_id = '@mbinuchannel'  

    # Initialize the Telegram bot
    telegram_bot = telegram.Bot(token=bot_token)

    try:
        response = None  # Initialize the response variable

        if image_filename is not None:
            # Send an image if it exists
            image_url = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            response = telegram_bot.send_photo(chat_id=channel_id, photo=open(image_url, 'rb'), caption=message_text)
            
            # Delete the temporary image file
            os.remove(image_url)
        else:
            # Send a text message if there is no image
            response = telegram_bot.send_message(chat_id=channel_id, text=message_text, parse_mode=telegram.ParseMode.HTML)

        if response:
            return f'Image and message sent to Telegram channel with message_id: {response.message_id}'
        else:
            return 'Message sent to Telegram channel.'

    except Exception as e:
        return f'Error sending image and message to Telegram channel: {str(e)}'

@newsletter_routes.route('/api/newsletters/<int:newsletter_id>', methods=['GET'])
def get_newsletter(newsletter_id):
    newsletter = newsletter_service.get_newsletter(newsletter_id)
    if newsletter:
        return jsonify(newsletter)
    else:
        return jsonify({'message': 'Newsletter not found'}), 404

@newsletter_routes.route('/api/newsletters/<int:newsletter_id>', methods=['PUT'])
def update_newsletter(newsletter_id):
    data = request.get_json()
    updated_newsletter = newsletter_service.update_newsletter(newsletter_id, data)
    if updated_newsletter:
        return jsonify({'message': 'Newsletter updated successfully', 'newsletter': updated_newsletter})
    else:
        return jsonify({'message': 'Newsletter not found'}), 404

@newsletter_routes.route('/api/newsletters/<int:newsletter_id>', methods=['DELETE'])
def delete_newsletter(newsletter_id):
    result = newsletter_service.delete_newsletter(newsletter_id)
    if result:
        return jsonify({'message': 'Newsletter deleted successfully'})
    else:
        return jsonify({'message': 'Newsletter not found'}), 404


@newsletter_routes.route('/api/set-token', methods=['POST'])
def set_bot_token_and_channel():

    data = request.get_json()
    bot_token = data.get('botToken')
    channel_id = data.get('channelID')
    # Get the current bot credentials from the database
    current_credentials = newsletter_service.get_bot_credentials()
    if bot_token or channel_id:
        # Update the credentials only if provided
        bot_token = bot_token or current_credentials.bot_token
        channel_id = channel_id or current_credentials.channel_id

        newsletter_service.create_or_update_bot_credentials(bot_token, channel_id)
        return jsonify({'message': 'Bot token and channel ID updated successfully'}), 200
    else:
        return jsonify({'error': 'Bot token or channel ID must be provided'}), 400
    


@newsletter_routes.route('/api/bot-credentials', methods=['GET'])
def fetch_bot_credentials():
    bot_token, channel_id = newsletter_service.get_bot_credentials()
    
    if bot_token and channel_id:
        return jsonify({'botToken': bot_token, 'channelID': channel_id}), 200
    else:
        return jsonify({'error': 'Bot credentials not found'}), 404
