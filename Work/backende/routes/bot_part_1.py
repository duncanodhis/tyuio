import logging
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext
from io import BytesIO
from services.address_service import AddressService
from flask import Blueprint, jsonify, request,current_app
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ConversationHandler, CallbackContext

from flask import Flask 
bot_routes = Blueprint('bot_routes', __name__)
address_service = AddressService()
# Enable logging (optional, but useful to see what's happening)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
# Define states for the conversation
EMOJI_VERIFICATION, HOME, LOCATION, CITY, DISTRICT , CATEGORY,PRODUCT ,GET_QUANTITY, CONFIRM_PURCHASE,DISTRICT_DELIVERY ,INSUFFICIENT_BALANCE, ASK_USERNAME, ASK_PASSWORD, CONFIRM_PASSWORD,SIGN_UP, SIGN_IN, ACCOUNT_DETAILS = range(17)
# Emojis for ve rification
emojis = ['👍', '👌', '😊', '🎉', '🍕', '🌟', '🐢', '🌈', '🎵', '🚀', '🍦', '🐳', '🏀', '🌺', '📚', '🍔']
# Function to start the conversation
def start(update: Update, context: CallbackContext) -> int:
    # Instructions to be shown to the user
    instructions = "Please select one emoji to verify that you are not a bot:"
    
    # Randomly select one emoji for verification
    verification_emoji = random.choice(emojis)
    context.user_data['verification_emoji'] = verification_emoji
    context.user_data['attempts_left'] = 3  # Reset attempts count
    
    # Arrange emojis in rows with three buttons per row
    emoji_buttons = [
        [InlineKeyboardButton(emoji, callback_data=emoji) for emoji in emojis[i:i+3]]
        for i in range(0, len(emojis), 3)
    ]
    # Add the verification emoji back to the list for the next attempt
    emojis.append(verification_emoji)

    # Add "Cancel" and "Back" buttons to the keyboard
    emoji_buttons.append([InlineKeyboardButton("Cancel", callback_data="❌"), InlineKeyboardButton("Back", callback_data="🔙")])

    reply_markup = InlineKeyboardMarkup(emoji_buttons)
    update.message.reply_text(f"{instructions}\n\n({verification_emoji} will verify you)", reply_markup=reply_markup)
    return EMOJI_VERIFICATION

def emoji_verification(update: Update, context: CallbackContext) -> int:
    user_choice = update.callback_query.data
    verification_emoji = context.user_data['verification_emoji']
    update.callback_query.answer()  # Acknowledge the button press

    # Check if the user selected the correct emoji
    if user_choice == verification_emoji:
        update.callback_query.message.reply_text(f"Great choice! You selected {user_choice}. You are verified. Welcome to the home page!")
        reset_verification_data(context)  # Reset verification data
        return home(update, context)  # Transition to the home page
    else:
        # Decrement the attempts left
        if 'attempts_left' not in context.user_data:
            context.user_data['attempts_left'] = 3
        context.user_data['attempts_left'] -= 1

        if context.user_data['attempts_left'] <= 0:
            update.callback_query.message.reply_text("Verification failed. You have been locked out.")
            reset_verification_data(context)  # Reset verification data
            return start(update, context)  # Retry verification
        else:
            update.callback_query.message.reply_text(f"Incorrect emoji selected. Please try again. ({context.user_data['attempts_left']} attempts left.")

            # Remove the selected emoji from the list
            emojis.remove(user_choice)

            # Show the keyboard with remaining attempts and the emoji to select
            emoji_buttons = [
                [InlineKeyboardButton(emoji, callback_data=emoji) for emoji in emojis[i:i + 3]]
                for i in range(0, len(emojis), 3)
            ]

            # Add the verification emoji back to the list for the next attempt
            emojis.append(verification_emoji)

            reply_markup = InlineKeyboardMarkup(emoji_buttons)
            update.callback_query.message.reply_text(f"Please select {verification_emoji} to verify that you are not a bot:", reply_markup=reply_markup)

            return EMOJI_VERIFICATION

def reset_verification_data(context: CallbackContext):
    # Reset verification data
    if 'verification_emoji' in context.user_data:
        del context.user_data['verification_emoji']
    if 'attempts_left' in context.user_data:
        del context.user_data['attempts_left']

def home(update: Update, context: CallbackContext) -> int:
    if update.message:
        user_id = update.message.chat_id
        username = update.message.from_user.username
        if username is None:
            username="avatar"
        print([user_id,username])
    elif update.callback_query:
        user_id = update.callback_query.message.chat_id
        username = update.callback_query.from_user.username
        # name = update.callback_query.from_user.first_name
        if username is None:
            username="avatar"
        print([user_id,username])
    else:
        return
    print("userid",user_id)
    print("username",username)
    # handle_start_button(user_id,username,app)
    gif_url = 'https://media.giphy.com/media/trN9ht5RlE3Dcwavg2/giphy.gif'
    context.bot.send_animation(chat_id=user_id, animation=gif_url)

    # Create a welcome message and inline keyboard with options
    message = 'Welcome {} to the Auto-Shop Bot! How can we help you today?'.format(username)
    keyboard = [[InlineKeyboardButton('Location', callback_data='location'),
                InlineKeyboardButton('Balance', callback_data='balance')],
                [InlineKeyboardButton('Profile', callback_data='profile'),
                InlineKeyboardButton('Last Order', callback_data='last_order')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send a new message to replace the old one
    message_sent = context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)

    # Edit the message to show only the button that was clicked
    query = update.callback_query
    if query:
        context.bot.edit_message_text(chat_id=user_id, 
                                      message_id=message_sent.message_id,
                                      text=query.data)

    # Use `context` instead of `update.message`
    context.bot.send_message(update.effective_chat.id, text=message, reply_markup=reply_markup)

    return HOME
def profile(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text("You selected Profile.")

def balance(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text("You selected Balance.")

def last_order(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text("You selected Last Order.")

def location(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_chat.id
    # Fetch addresses from the endpoint
    addresses_endpoint = 'http://127.0.0.1:5000/api/addresses'
    try:
        response = requests.get(addresses_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        addresses = response.json()
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=user_id, text='Failed to fetch addresses. Please try again later.')
        return HOME
    # Convert the addresses data to a list of countries
    countries = [address["country"] for address in addresses]
    message = "Select your country of location:"
    keyboard = [[InlineKeyboardButton(country, callback_data=f'country-{country}')] for country in countries]
    keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)

    return LOCATION

def country_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_country = query.data.split('-')[1]

    # Make an HTTP request to fetch cities in the selected country
    cities_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities'
    print(cities_endpoint)
    try:
        response = requests.get(cities_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        cities = response.json()
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch cities. Please try again later.')
        return LOCATION

    # Convert the cities data to a list
    city_names = [city for city in cities]

    # Store the selected country in context.user_data to use it in the next step
    context.user_data['selected_country'] = selected_country

    message = f"Selected country: {selected_country}\nNow, choose a city within {selected_country}:"
    keyboard = [[InlineKeyboardButton(city, callback_data=f'city-{city}')] for city in city_names]
    keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
    return CITY

def city_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_city = query.data.split('-')[1]

    # Make an HTTP request to fetch districts in the selected city of the selected country
    selected_country = context.user_data.get('selected_country')
    districts_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/districts'  # Updated endpoint URL
    try:
        response = requests.get(districts_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        districts = response.json()
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch districts. Please try again later.')
        return CITY

    # Convert the districts data to a list
    district_names = [district for district in districts]
    # Store the selected city in context.user_data to use it in the next step
    context.user_data['selected_city'] = selected_city

    # Make an HTTP request to fetch categories in the selected city
    categories_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/categories'
    try:
        response = requests.get(categories_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        categories = response.json()
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch categories. Please try again later.')
        return CITY

    # Extract category names from the list of category dictionaries
    category_names = [category["name"] for category in categories]

    # Store the selected city and categories in context.user_data to use them in the next step
    context.user_data['selected_city'] = selected_city
    context.user_data['categories'] = categories

    message = f"Selected city: {selected_city}\nChoose a category of products in {selected_city}:"
    keyboard = [[InlineKeyboardButton(category, callback_data=f'category-{category}')] for category in category_names]
    keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
    return CATEGORY

def district_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id
    selected_district = query.data.split('-')[1]

    # Retrieve the selected product details from context.user_data
    selected_product = context.user_data.get('selected_product')

    if selected_product:
        try :
            # Extract product details
            product_name = selected_product['name']
            product_price = selected_product['selling_price']
            product_currency = selected_product['selling_currency']
            selling_weight = selected_product['selling_weight']
            selling_weight_measurement = selected_product['selling_weight_measurement']
            selling_description  = selected_product['selling_description']

            # Show the product details to the user
            message = f"You selected {product_name}.\n Product description:{selling_description }\nThe product quantity is {selling_weight} {selling_weight_measurement}.\nThe price is {product_price} {product_currency}.\nEnter the quantity of {product_name}(s) you want to purchase:"
            context.bot.send_message(chat_id=query.message.chat_id, text=message)
            # Ask the user to select a district for delivery
            # Fetch districts in the selected city of the selected country
            selected_country = context.user_data.get('selected_country')
            selected_city = context.user_data.get('selected_city')
            districts_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/districts'
            response = requests.get(districts_endpoint)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            districts = response.json()
            context.bot.send_message(chat_id=user_id, text=message)
            return GET_QUANTITY
        
        except requests.RequestException as e:
            # Handle the error, e.g., show an error message to the user
            context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch districts. Please try again later.')
            return DISTRICT
        
    else:
        # If the product is not found, show an error message
        context.bot.send_message(chat_id=query.message.chat_id, text='Product not found. Please try again.')
        return CATEGORY

def delivery_district_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id

    # Retrieve the selected delivery district from the user's response
    selected_delivery_district = query.data.split('-')[1]

    # Store the selected delivery district in context.user_data to use it in the next step
    context.user_data['selected_delivery_district'] = selected_delivery_district

    # Retrieve the product details and other data from context.user_data
    selected_product = context.user_data.get('selected_product')
    quantity = context.user_data.get('quantity')
    total_cost = context.user_data.get('total_cost')

    # Create a message with the product details, delivery district, and total cost
    message = f"Product: {selected_product['name']}\nSelling Price: {selected_product['selling_price']} {selected_product['selling_currency']}\nQuantity: {quantity} {selected_product['selling_weight_measurement']}\nDescription: {selected_product['selling_description']}\nDelivery District: {selected_delivery_district}\nTotal Cost: {total_cost} {selected_product['selling_currency']}\n\nDo you want to proceed with the purchase?"
    keyboard = [[InlineKeyboardButton("Yes", callback_data="confirm_purchase"),
                 InlineKeyboardButton("No", callback_data="cancel_purchase")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)
    return CONFIRM_PURCHASE

def category_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_category = query.data.split('-')[1]

    # Retrieve the selected category details from context.user_data
    categories = context.user_data.get('categories', [])
    print("categories:", categories)
    selected_category_data = next((category for category in categories if category['name'] == selected_category), None)

    if selected_category_data:
        # Extract category details
        category_id = selected_category_data['id']

        # Make an HTTP request to fetch products in the selected category
        selected_country = context.user_data.get('selected_country')
        selected_city = context.user_data.get('selected_city')
        products_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/categories/{category_id}/products'
        try:
            response = requests.get(products_endpoint)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            products = response.json()
        except requests.RequestException as e:
            # Handle the error, e.g., show an error message to the user
            context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch products. Please try again later.')
            return CATEGORY

        # Convert the products data to a list
        product_names = [product['name'] for product in products]

        # Store the selected category and products in context.user_data to use them in the next step
        context.user_data['selected_category'] = selected_category
        context.user_data['products'] = products

        message = f"Selected category: {selected_category}\nChoose a product within {selected_category}:"
        keyboard = [[InlineKeyboardButton(product, callback_data=f'product-{product}')] for product in product_names]
        keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
        return PRODUCT
    else:
        # If the selected category is not found, show an error message
        context.bot.send_message(chat_id=query.message.chat_id, text='Category not found. Please try again.')

    return CATEGORY

def product_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id

    # Retrieve the selected product name from the user's response
    selected_product_name = query.data.split('-')[1]

    # Fetch the details of the selected product from the endpoint
    selected_country = context.user_data.get('selected_country')
    selected_city = context.user_data.get('selected_city')
    selected_category_name = context.user_data.get('selected_category')    
    # print("selected_category_data",selected_category_data)
     # Find the selected category in the list of categories fetched from the endpoint
    categories = context.user_data.get('categories', [])
    selected_category_data = next((category for category in categories if category['name'] == selected_category_name), None)

    if selected_category_data:
        category_name = selected_category_data['id']
        products_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/categories/{category_name}/products'
        try:
            response = requests.get(products_endpoint)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            products = response.json()
        except requests.RequestException as e:
            # Handle the error, e.g., show an error message to the user
            context.bot.send_message(chat_id=user_id, text='Failed to fetch products. Please try again later.')
            return PRODUCT

        # Find the selected product in the list of products fetched from the endpoint
        selected_product = next((product for product in products if product['name'] == selected_product_name), None)
        # print(selected_product)
        if selected_product:
            # Extract product details
            product_name = selected_product['name']
            product_price = selected_product['selling_price']
            product_currency = selected_product['selling_currency']
            selling_weight = selected_product['selling_weight']
            selling_weight_measurement = selected_product['selling_weight_measurement']
            selling_description  = selected_product['selling_description']
            
            districts_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/districts'
            response = requests.get(districts_endpoint)
            response.raise_for_status()  # Raise an exception if the response status code is not 2xx
            districts = response.json()
            # Store the selected product details and quantity in context.user_data to use them in the next step
            context.user_data['selected_product'] = selected_product
            
            # Ask the user for the quantity of the selected product
            message = f"You selected {product_name}.\n Product description:{selling_description }\nThe product quantity is {selling_weight} {selling_weight_measurement}.\nThe price is {product_price} {product_currency}.\n Select the District of delivery:"
            keyboard = [[InlineKeyboardButton(district, callback_data=f'district-{district}')] for district in districts]
            keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
            

            return DISTRICT
        else:
            # If the selected product is not found, show an error message
            context.bot.send_message(chat_id=user_id, text='Product not found. Please try again.')
            return CATEGORY
    else:
        # If the selected category is not found, show an error message
        context.bot.send_message(chat_id=user_id, text='Category not found. Please try again.')
        return CATEGORY

def get_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id

    # Retrieve the quantity from the user's response
    quantity = update.message.text
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError()
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Invalid quantity. Please enter a positive number.")
        return GET_QUANTITY

    # Store the quantity in context.user_data to use it in the next step
    context.user_data['quantity'] = quantity

    # Calculate the total cost
    selected_product = context.user_data.get('selected_product')
    if selected_product:
        product_price = selected_product['selling_price']
        total_cost = quantity * product_price

        # Store the total cost in context.user_data to use it in the next step
        context.user_data['total_cost'] = total_cost

        # Show the total cost to the user and ask for confirmation
        message = f"You selected {quantity} {selected_product['name']}(s).\nTotal Cost: {total_cost} {selected_product['selling_currency']}\nDo you want to proceed with the purchase?"
        keyboard = [[InlineKeyboardButton("Yes", callback_data="confirm_purchase"),
                     InlineKeyboardButton("No", callback_data="cancel_purchase")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)
        return CONFIRM_PURCHASE
    else:
        # If the product is not found, show an error message
        context.bot.send_message(chat_id=user_id, text='Product not found. Please try again.')
        return CATEGORY
