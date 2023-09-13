import logging
import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
import random  # Don't forget to add this line for the 'random' module
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
import requests
from telegram import InputFile
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot states
CHOOSING, REVIEWS, ORDERS, DISPUTES, URGENCY, DISPUTE_COMMENT = range(6)

# Dictionary to store user data
user_data = {}

# Function to start the bot
def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_data[user_id] = {}
    
    # Get the username of the user
    username = update.message.from_user.username
    
    # Define emojis and a happy tone
    emojis = ['😃', '🌟', '🎉', '👍']
    happy_tone = random.choice(emojis)
    
    reply_keyboard = [['Reviews', 'Disputes']]
    
    # Customize the welcome message with the username, emojis, and happy tone
    welcome_message = f"Hello, @{username}! {happy_tone} 😊\n\n"
    welcome_message += "Welcome to the Review and Dispute Bot! How can we assist you today? 🤝"
    
    update.message.reply_text(
        welcome_message,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    
    return CHOOSING

# Function to fetch orders by Telegram ID (Replace with your actual query)
def get_orders_by_telegram_id(telegram_id):
    # URL of the Flask API route for fetching orders by Telegram ID
    api_url = f'http://127.0.0.1:5000/api/orders/telegram/{telegram_id}' 
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            orders = response.json()  # Assuming your API returns JSON data
            return orders
        else:
            print(f"Error fetching orders: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to list orders and ask for reviews or disputes
def reviews_or_disputes(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    choice = update.message.text
    user_data[user_id]['choice'] = choice
    orders = get_orders_by_telegram_id(user_id)

    if orders is None:
        update.message.reply_text("❌ Failed to fetch your orders. Please try again later.")
        return ConversationHandler.END

    if not orders:
        update.message.reply_text("📭 No orders found for this Telegram username.")
        return ConversationHandler.END

    user_data[user_id]['orders'] = orders

    # Create a message to display order details
    order_details_message = "📦 Here are your orders:\n\n"
    for order in orders:
        order_details_message += f"📋 Order ID: {order['id']}\n"
        order_details_message += f"📦 Product: {order['product_name']}\n"
        order_details_message += f"🛒 Status: {order['payment_status']}\n"
        order_details_message += f"💰 Paid: {order['payment_status']}\n"
        order_details_message += f"💲 Purchase Price: {order['total_price']}\n"
        order_details_message += f"📊 Quantity: {order['quantity']} {order['quantity_unit']}\n\n"

    update.message.reply_text(order_details_message)

    reply_keyboard = [[order['id']] for order in orders]
    update.message.reply_text(
        "📝 Please select an order to review or file a dispute:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return ORDERS

# Function to handle selected order for review or dispute
def order_selected(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    selected_order = update.message.text
    user_data[user_id]['selected_order'] = selected_order
    product_id = fetch_product_id_from_order(user_data[user_id]['selected_order'])
    user_data[user_id]['selected_order_product_id'] = product_id

    choice = user_data[user_id]['choice']

    if choice == "Disputes":
        update.message.reply_text("😢 Please rate the urgency of your dispute (1-5):\n\n"
                                  "Example ratings:\n"
                                  "1️⃣ - Not very urgent\n"
                                  "3️⃣ - Moderately urgent\n"
                                  "5️⃣ - Extremely urgent")
        return URGENCY
    else:
        update.message.reply_text(f"😥 You selected {selected_order}. It's okay, please provide a rating (1-5):\n\n"
                                  "Example ratings:\n"
                                  "1️⃣ - Poor\n"
                                  "3️⃣ - Average\n"
                                  "5️⃣ - Excellent")
        return REVIEWS

# Function to fetch product ID from the order (Replace with your actual logic)
def fetch_product_id_from_order(order_id):
    # Define the URL of the endpoint
    endpoint_url = f'http://127.0.0.1:5000/api/orders/{order_id}'
    try:
        # Send a GET request to the endpoint
        response = requests.get(endpoint_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            order_data = response.json()  # Assuming the endpoint returns JSON data
            product_id = order_data.get('product_id')
            
            if product_id is not None:
                return product_id
            else:
                return None  # Product ID not found in the response
        else:
            print(f"Error fetching order data: {response.status_code}")
            return None  # Request failed
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None  

# Function to post data to the reviews endpoint
def post_to_reviews_backend(user_id, selected_order_id, product_id, rating, comments):
    # Prepare the data to send to the reviews endpoint
    data = {
        'user_id': user_id,
        'selected_order_id': selected_order_id,
        'product_id': product_id,
        'rating': rating,
        'comments': comments
    }
    # Make a POST request to your reviews endpoint (Replace with your actual URL)
    response = requests.post('http://127.0.0.1:5000/api/reviews', json=data)
    if response.status_code == 200:
        return True
    else:
        return False

# Function to post data to the disputes endpoint
def post_to_disputes_backend(user_id, selected_order_id, urgency, dispute_text):
    # Prepare the data to send to the disputes endpoint
    data = {
        'telegram_id': user_id,
        'order_id': selected_order_id,
        'urgency': urgency,
        'message': dispute_text
    }
    # Make a POST request to your disputes endpoint (Replace with your actual URL)
    response = requests.post('http://127.0.0.1:5000/api/disputes', json=data)
    if response.status_code == 200:
        return True
    else:
        return False


# Function to handle ratings
def rate_order(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    rating = update.message.text
    user_data[user_id]['rating'] = rating

    # Provide an example for the user to understand the rating and comments
    example_message = "🌟 You rated the order with " + rating + " stars! Great choice! 🌟\n\n"
    example_message += "Now, please provide your comments for the order. 📝\n"
    example_message += "Example comment: 'The product quality was excellent and the delivery was fast.' 💬"

    update.message.reply_text(example_message)
    return DISPUTE_COMMENT


# Function to handle urgency ratings for disputes
def rate_urgency(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    urgency = update.message.text
    user_data[user_id]['urgency'] = urgency

    # Provide an example for the user to understand the urgency of your dispute 
    example_message = "Example urgency message:\n"\
                      "I received a damaged product and need a replacement ASAP. 😟"


    update.message.reply_text("😟Please enter your dispute message.\n\n" + example_message)
    return DISPUTE_COMMENT


# Function to handle collecting comments and posting reviews or disputes
def collect_comments(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    comments = update.message.text
    user_data[user_id]['comments'] = comments

    choice = user_data[user_id]['choice']

    if choice == "Disputes":
        # Post the data to the disputes backend
        selected_order_id = user_data[user_id]['selected_order']
        urgency = user_data[user_id]['urgency']
        if post_to_disputes_backend(user_id, selected_order_id, urgency, comments):
            update.message.reply_text("🛡️ Thank you for your dispute! We have received it. 🙏")
            update.message.reply_text("🚀 We are working to resolve the dispute, and you will be updated soon. 🕒")
        else:
            update.message.reply_text("❌ Failed to submit your dispute. Please try again later. 😞")
    else:
        # Post the data to the reviews backend
        selected_order_id = user_data[user_id]['selected_order']
        rating = user_data[user_id]['rating']
        comments = user_data[user_id]['comments']
        product_id = user_data[user_id]['selected_order_product_id'] 

        if post_to_reviews_backend(user_id, selected_order_id, product_id, rating, comments):
            update.message.reply_text("🌟 Thank you for your review! We have received it. 😊")
            update.message.reply_text("🙌 We appreciate your feedback! Please consider referring our products to other clients. 🤝")
        else:
            update.message.reply_text("❌ Failed to submit your review. Please try again later. 😞")
    
    return ConversationHandler.END

# Function to handle unknown commands
def unknown(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Sorry, I didn't understand that command.")
    return ConversationHandler.END

def get_reviews_and_disputes_bot_token():
    try:
        response = requests.get('http://127.0.0.1:5000/api/latest/disputes_reviews_bot')
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print('Failed to fetch Reviews Bot token:', response.status_code)
    except Exception as e:
        print('Error:', e)
    return None

def main():
    reviews_and_disputes_bot = get_reviews_and_disputes_bot_token()
    updater = Updater(token=reviews_and_disputes_bot, use_context=True)  # Replace with your bot token
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^(Reviews|Disputes)$'), reviews_or_disputes),
                MessageHandler(Filters.text & ~Filters.regex('^(Reviews|Disputes)$'), unknown),
            ],
            ORDERS: [
                MessageHandler(Filters.text & ~Filters.regex('^(Reviews|Disputes)$'), order_selected),
            ],
            URGENCY: [
                MessageHandler(Filters.regex(r'^[1-5]$'), rate_urgency),
            ],
            REVIEWS: [
                MessageHandler(Filters.text & Filters.regex(r'^[1-5]$'), rate_order),
            ],
            DISPUTE_COMMENT: [
                MessageHandler(Filters.text & ~Filters.regex('^(Reviews|Disputes)$'), collect_comments),
            ],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
