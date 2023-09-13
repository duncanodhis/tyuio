import logging
import random
from PIL import Image
import requests
from telegram import InputFile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
from flask import Blueprint, jsonify, request,current_app
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ConversationHandler, CallbackContext
import os
from flask import Flask 

bot_routes = Blueprint('bot_routes', __name__)
# address_service = AddressService()
# Enable logging (optional, but useful to see what's happening)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
# Define states for the conversation
EMOJI_VERIFICATION, HOME, LOCATION, CITY, DISTRICT , CATEGORY,PRODUCT,GET_QUANTITY, CONFIRM_PURCHASE,DISTRICT_DELIVERY ,INSUFFICIENT_BALANCE, ASK_USERNAME, ASK_PASSWORD,SIGN_UP, SIGN_IN, ACCOUNT_DETAILS , ASK_PASSWORD2 = range(17)
CONFIRM_PASSWORD = 3
# Emojis for verification
emojis = ['👍', '👌', '😊', '🎉', '🍕', '🌟', '🐢', '🌈', '🎵', '🚀', '🍦', '🐳', '🏀', '🌺', '📚', '🍔']
# Function to start the conversation
user_signup_data = {}
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
    # emoji_buttons.append([InlineKeyboardButton("Cancel", callback_data="❌"), InlineKeyboardButton("Back", callback_data="🔙")])

    reply_markup = InlineKeyboardMarkup(emoji_buttons)
    update.message.reply_text(f"{instructions}\n\n({verification_emoji} will verify you)", reply_markup=reply_markup)
    return EMOJI_VERIFICATION

def emoji_verification(update: Update, context: CallbackContext) -> int:
    user_choice = update.callback_query.data
    
    user_id = update.callback_query.from_user.id
    username = update.callback_query.from_user.username
    user_profile_photos = context.bot.get_user_profile_photos(user_id=user_id)

    # Check if the user has profile photos
    if user_profile_photos.total_count > 0:
        # Get the latest profile photo
        latest_profile_photo = user_profile_photos.photos[0][-1]

        # Get the file object for the profile photo
        file = context.bot.get_file(latest_profile_photo.file_id)

        # Specify the directory to save the profile picture
        save_directory = "/images"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Download the file and save it as an image in the specified directory
        selected_user_profile = os.path.join(save_directory, f"user_{user_id}.jpg")
        file.download(selected_user_profile)
    verification_emoji = context.user_data['verification_emoji']
    update.callback_query.answer()  # Acknowledge the button press

    # Check if the user selected the correct emoji
    if user_choice == verification_emoji:
        update.callback_query.message.reply_text(f"Great choice! You selected {user_choice}. You are verified. Welcome to the home page!")
        reset_verification_data(context)  
        if check_account_endpoint(user_id)== True:
            context.bot.send_message(chat_id=user_id, text="Please provide your username:")
            return ASK_USERNAME
        else :
            telegram_username = username
            message_text = f"Hello @{telegram_username}, we are excited to create your account! To proceed, we kindly request your password. Please provide it here:"
            user_signup_data[user_id] = {"username": username}
            context.bot.send_message(chat_id=user_id, text=message_text)
            return "USERNAME"
        
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

def check_account_endpoint(user_id):
    # Replace this with your actual endpoint URL and logic to check the account
    api_url = f"http://127.0.0.1:5000/api/customer/{user_id}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Check the HTTP status code to determine if the customer was found or not
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            return False  # Return False for any other non-successful status codes

    except requests.exceptions.RequestException as e:
        # Catch any request-related exception (e.g., ConnectionError, Timeout, etc.)
        return False
    except requests.exceptions.HTTPError as e:
        # Catch HTTP error (e.g., 404 Not Found, 500 Internal Server Error, etc.)
        return False
    except requests.exceptions.JSONDecodeError as e:
        # Catch JSON decoding error if the response is not a valid JSON
        return False
    except Exception as e:
        # Catch any other unexpected exception
        return False

def ask_username(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id
    username = update.message.text

    # Store the username in the user_data
    context.user_data['username'] = username

    # Ask the user to provide their password
    context.bot.send_message(chat_id=user_id, text="Please enter your password:")

    # Return the next state, which is asking for the password
    return ASK_PASSWORD

def ask_password(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id
    password = update.message.text

    # Store the password in the user_data
    context.user_data['password'] = password

    # Retrieve the username from user_data (assuming it's already stored there)
    username = context.user_data.get('username')

    # Call the function to check the account with the captured username and password
    authenticated, customer_data = authenticate_user(username, password)

    # Handle the authentication result
    if authenticated:
        # Authentication was successful, return to the "home" state
        return home(update, context)
    else:
        # Authentication failed, end the conversation
        update.message.reply_text("Authentication failed. Please try again or /start over.")
        return ConversationHandler.END

def authenticate_user(username, password):
    url = 'http://localhost:5000/api/authenticate'  # Update with the correct URL
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # Authentication was successful
        data = response.json()
        customer_data = data.get('customer')
        if customer_data is not None:
            return True, customer_data
        else:
            # Authentication failed
            return False, None
    elif response.status_code == 401:
        print("Authentication failed:", response.json()['message'])
        return False, None
    elif response.status_code == 404:
        print("User not found:", response.json()['message'])
        return False, None
    else:
        print("An error occurred:", response.status_code)
        return False, None

def ask_password_sign_up(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_signup_data[user_id] = {"username": context.user_data.get("username")}
    user_id = update.message.from_user.id
    user_input = update.message.text.strip()
    user_signup_data[user_id]["password"] = user_input 
    context.bot.send_message(chat_id=user_id, text="Please set your password:")
    return CONFIRM_PASSWORD

def confirm_password(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_input = update.message.text.strip()
    password = user_signup_data[user_id].get("password")
    username = update.message.from_user.username
  
    if password == user_input:
     
        # Save user details in the database using a POST request
        data = {
            "telegram_id":user_id,
            "username": username,
            "password": password, 
        }
        # print(data)
        api_endpoint =  f'http://127.0.0.1:5000/api/customers'
        try:
            response = requests.post(api_endpoint, json=data)
            response.raise_for_status()
            # Passwords match, registration is successful
            context.bot.send_message(chat_id=user_id, text="Password confirmed. Registration successful!")
            return home(update,context)
        except requests.RequestException as e:
            # Handle the error, e.g., show an error message to the user
            context.bot.send_message(chat_id=user_id, text=f"Error occurred while saving user details: {e}")

        # Clear the user data after successful registration
        del user_signup_data[user_id]
        context.user_data.clear()
    else:
        context.bot.send_message(chat_id=user_id, text="Passwords do not match. Please try again.")
        return CONFIRM_PASSWORD

def reset_verification_data(context: CallbackContext):
    # Reset verification data
    if 'verification_emoji' in context.user_data:
        del context.user_data['verification_emoji']
    if 'attempts_left' in context.user_data:
        del context.user_data['attempts_left']

def home(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id
    username = context.user_data.get('username')
    message = f'Welcome {username} to the Auto-Shop Bot! How can we help you today?'

    keyboard = [[InlineKeyboardButton('Location', callback_data='location'),
                 InlineKeyboardButton('Balance', callback_data='balance')],
                [InlineKeyboardButton('Profile', callback_data='profile'),
                 InlineKeyboardButton('Last Order', callback_data='last_order')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)
    return HOME

def profile(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id  # Use 'effective_user.id' to get the user ID
    username = context.user_data.get('username')

    # Get the wallet balance
    get_wallet_balance_endpoint = 'http://127.0.0.1:5000/api/get_balance'
    response = requests.get(get_wallet_balance_endpoint, json={'telegram_id': user_id})
    response_data = response.json()

    available_balance = response_data.get('available_balance')
    address = response_data.get('address')

    if available_balance is not None:
        msg = f"👤 Account Details\n\n"
        msg += f"🔹 Username: {username}\n"
        msg += f"💰 Available Balance: {available_balance} BTC\n"
        msg += f"🏦 Wallet Address: {address}\n"
        context.bot.send_message(chat_id=user_id, text=msg)
    else:
        context.bot.send_message(chat_id=user_id, text="Unable to retrieve wallet balance. Please try again later.")

    return ConversationHandler.END

def balance(update: Update, context: CallbackContext) -> int:
        user_id = update.callback_query.from_user.id
        # user_response = update.message.text.lower()
        get_wallet_balance_endpoint = 'http://127.0.0.1:5000/api/get_balance'
        response = requests.get(get_wallet_balance_endpoint, json={'telegram_id': user_id})
        response_data = response.json()
        # print("response data for balance",response_data)
        available_balance = response_data.get('available_balance', "N/A")
        address = response_data.get('address', "N/A")

        if address:
            msg = f"\n💰 Available Balance BTC: {available_balance} .\n🏦 Your Wallet Address: {address}\n"
            context.bot.send_message(chat_id=user_id, text=msg)
        
        return ConversationHandler.END

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
    # Convert the addresses data to a list of unique countries
    unique_countries = list(set(address['country'] for address in addresses))
    message = "Select your country of location:"
    keyboard = [[InlineKeyboardButton(country, callback_data=f'country-{country}')] for country in unique_countries]
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)

    return LOCATION

def country_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_country = query.data.split('-')[1]
    # print(selected_country)
    # Make an HTTP request to fetch cities in the selected country
    cities_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities'
    # print(cities_endpoint)
    try:
        response = requests.get(cities_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        cities = response.json()
        # print(cities)
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch cities. Please try again later.')
        return LOCATION

    # Convert the cities data to a list
    city_names = [city for city in cities]
    # print("city names",city_names)

    # Store the selected country in context.user_data to use it in the next step
    context.user_data['selected_country'] = selected_country

    message = f"Selected country: {selected_country}\nNow, choose a city within {selected_country}:"
    keyboard = [[InlineKeyboardButton(city, callback_data=f'city-{city}')] for city in city_names]
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # print(keyboard)
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
    return LOCATION

def city_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    # print("in the cities")
    selected_city = query.data.split('-')[1]
    # print(selected_city)
    # Make an HTTP request to fetch districts in the selected city of the selected country
    selected_country = context.user_data.get('selected_country')
    # Make an HTTP request to fetch categories in the selected city
    city_photo_url = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/photo'
    
    # Fetch the image data from the URL
    response = requests.get(city_photo_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
    else:
        # Handle the case where the image could not be fetched
        image_data = None

    # Send a message with the city image as a photo
    categories_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/categories'
    try:
        response = requests.get(categories_endpoint)
        response.raise_for_status()  # Raise an exception if the response status code is not 2xx
        categories = response.json()
        print(categories)
    except requests.RequestException as e:
        # Handle the error, e.g., show an error message to the user
        context.bot.send_message(chat_id=query.message.chat_id, text='Failed to fetch categories. Please try again later.')
        return LOCATION

    # Extract category names from the list of category dictionaries
    category_names = [category["name"] for category in categories]
    #  # Store the selected city in context.user_data to use it in the next step
    # context.user_data['selected_city'] = selected_city
    # Store the selected city and categories in context.user_data to use them in the next step
    context.user_data['selected_city'] = selected_city
    context.user_data['categories'] = categories
    
    # Send a message with the city image as a photo
    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=InputFile(image_data, filename='city_photo.jpg') if image_data else None,
        caption=f"Selected city: {selected_city}"
    )
    # Send the message with inline keyboard buttons
    message = f"Choose a category of products in {selected_city}:"
    keyboard = [[InlineKeyboardButton(category, callback_data=f'category-{category}')] for category in category_names]
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=message,
        reply_markup=reply_markup,
    )
    
    # context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup.to_dict())  # Convert InlineKeyboardMarkup to dictionary
    return CATEGORY

def district_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id
    selected_district = query.data.split('-')[1]

    # Retrieve the selected product details from context.user_data
    selected_product = context.user_data.get('selected_product')
    selected_country = context.user_data.get('selected_country')
    selected_city = context.user_data.get('selected_city')

    context.user_data['selected_district'] = selected_district
    district_photo_url = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/districts/{selected_district}/photo'
      # Fetch the image data from the URL
    response = requests.get(district_photo_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
    else:
        # Handle the case where the image could not be fetched
        image_data = None

    if selected_product:
        try :
            # Extract product details
            product_name = selected_product['name']
            product_price = selected_product['selling_price']
            product_currency = selected_product['selling_currency']
            selling_weight = selected_product['selling_weight']
            selling_weight_measurement = selected_product['selling_weight_measurement']
            selling_description  = selected_product['selling_description']
            
            context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=InputFile(image_data, filename='city_photo.jpg') if image_data else None,
                caption=f"Selected district: {selected_district}"
            )
            # Show the product details to the user
            message = f"You selected {product_name}.\n Product description:{selling_description }\nThe product quantity is {selling_weight} {selling_weight_measurement} located at {selected_district}.\nThe price is {product_price} {product_currency}.\nEnter the number of orders for product: {product_name}(s) you want to purchase:"
            # context.bot.send_message(chat_id=query.message.chat_id, text=message)
            # Ask the user to select a district for delivery
            # Fetch districts in the selected city of the selected country
            selected_country = context.user_data.get('selected_country')
            selected_city = context.user_data.get('selected_city')
            # selected_district = context.user_data.get('selected_district')
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
    # print("categories:", categories)
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
        unique_product = list(set([product['name'] for product in products]))

        # Store the selected category and products in context.user_data to use them in the next step
        context.user_data['selected_category'] = selected_category   
        context.user_data['products'] = products

        message = f"Selected category: {selected_category}\nChoose a product within {selected_category}:"
        keyboard = [[InlineKeyboardButton(product, callback_data=f'product-{product}')] for product in unique_product]
        keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
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
    selected_product_name = query.data.split('-')[1]

    # Fetch the details of the selected product from the endpoint
    selected_country = context.user_data.get('selected_country')
    selected_city = context.user_data.get('selected_city')
    selected_category_name = context.user_data.get('selected_category')
    categories = context.user_data.get('categories', [])
    selected_category_data = next((category for category in categories if category['name'] == selected_category_name), None)

    if selected_category_data:
        category_name = selected_category_data['id']
        products_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/categories/{category_name}/products'
        try:
            response = requests.get(products_endpoint)
            response.raise_for_status()
            products = response.json()
        except requests.RequestException as e:
            context.bot.send_message(chat_id=user_id, text='Failed to fetch products. Please try again later.')
            return PRODUCT
   
        selected_product = next((product for product in products if product['name'] == selected_product_name), None)
        if selected_product:
            product_name = selected_product['name']
            product_price = selected_product['selling_price']
            product_currency = selected_product['selling_currency']
            selling_weight = selected_product['selling_weight']
            selling_weight_measurement = selected_product['selling_weight_measurement']
            selling_description = selected_product['selling_description']
            selected_product_packag_id = selected_product['package_id']
            context.user_data['product_currency']= product_currency
            product_photo_url = f'http://127.0.0.1:5000/api/packages/{selected_product_packag_id}/photo'
            
            response = requests.get(product_photo_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                target_size = (300, 300)
                image.thumbnail(target_size)
                image_data = BytesIO()
                image.save(image_data, format='JPEG')
                image_data.seek(0)
            else:
                image_data = None
                
            districts_endpoint = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/districts'
            response = requests.get(districts_endpoint)
            response.raise_for_status()
            districts = response.json()

            context.user_data['selected_product'] = selected_product
            context.user_data['selected_selling_weight'] = selling_weight 
           
            context.user_data['selected_selling_weight_measurement'] = selling_weight_measurement
            context.user_data['selected_product_packag_id'] = selected_product_packag_id
            
            message = (
                f"You selected {product_name}.\n"
                f"Product description: {selling_description}\n"
                f"The product quantity is {selling_weight} {selling_weight_measurement}.\n"
                f"The price is {product_price} {product_currency}.\n"
                "Select the District of delivery:"
            )
            keyboard = [[InlineKeyboardButton(district, callback_data=f'district-{district}')] for district in districts]
            keyboard.append([InlineKeyboardButton("Back", callback_data="🔙")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=InputFile(image_data, filename='product_photo.jpg') if image_data else None,
                caption=f"Selected product: {product_name}\nPrice { product_price }{product_currency}\n Weight:{ selling_weight}{selling_weight_measurement}\nDescription:{selling_description}",
                reply_markup=reply_markup,
            )
            return DISTRICT
        else:
            context.bot.send_message(chat_id=user_id, text='Product not found. Please try again.')
            return CATEGORY
    else:
        context.bot.send_message(chat_id=user_id, text='Category not found. Please try again.')
        return CATEGORY

def get_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id
    # Retrieve the quantity from the user's response
    number_of_orders = update.message.text
    try:
        number_of_orders = int(number_of_orders)
        context.user_data['number_of_orders'] = number_of_orders
        if number_of_orders <= 0:
            raise ValueError()
    except ValueError:
        context.bot.send_message(chat_id=user_id, text="Invalid quantity. Please enter a positive number.")
        return GET_QUANTITY

    # Store the quantity in context.user_data to use it in the next step
    context.user_data['number_of_orders'] = number_of_orders

    # Calculate the total cost
    selected_product = context.user_data.get('selected_product')
    if selected_product:
        product_price = selected_product['selling_price']
        total_cost = number_of_orders * product_price

        # Make an HTTP POST request to the /calculate_discount endpoint
        url = 'http://localhost:5000/api/calculate_discount'  # Update the URL if needed
        data = {
            'total_cost': total_cost,
            'product_name': selected_product['name'],
            'number_of_purchases': number_of_orders
        }
        
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            discounted_cost = result.get('discounted_cost')
            # Store the discounted cost in context.user_data to use it in the next step
            context.user_data['total_cost'] = discounted_cost
            
            # Show the total cost to the user and ask for confirmation
            message = f"🎉 Yay! You've selected {number_of_orders} {selected_product['name']}{'s' if number_of_orders > 1 else ''}! 🛍️\n"
            message += f"Total Cost: {discounted_cost} {selected_product['selling_currency']} 💰\n"
            message += "Are you excited to proceed with your purchase? 🚀"
            keyboard = [[InlineKeyboardButton("Yes", callback_data="confirm_purchase"),
                         InlineKeyboardButton("No", callback_data="cancel_purchase")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)
            return CONFIRM_PURCHASE
        else:
            context.bot.send_message(chat_id=user_id, text='Failed to calculate discount. Please try again.')
            return CATEGORY
    else:
        # If the product is not found, show an error message
        context.bot.send_message(chat_id=user_id, text='Product not found. Please try again.')
        return CATEGORY

def confirm_purchase(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if not query or not query.message:
        # The callback query or the associated message is None, handle the error
        context.bot.send_message(chat_id=update.effective_chat.id, text="Something went wrong. Please try again later.")
        return ConversationHandler.END

    selected_district = context.user_data.get('selected_district')
    selected_country = context.user_data.get('selected_country')
    selected_city = context.user_data.get('selected_city')
    selected_selling_weight = context.user_data.get('selected_selling_weight')
    selected_selling_weight_measurement = context.user_data.get('selected_selling_weight_measurement')
    selected_product_packag_id = context.user_data.get('selected_product_packag_id')
    user_id = query.message.chat_id

    # Retrieve address details
    address = f'http://127.0.0.1:5000/api/countries/{selected_country}/cities/{selected_city}/{selected_district}'
    response_for_address = requests.get(address)
    response_for_address.raise_for_status()
    addressdetails = response_for_address.json()
    address_id = addressdetails["id"]

    # Retrieve product details
    product = f'http://127.0.0.1:5000/api/product/{selected_product_packag_id}/{address_id}'
    response_for_product = requests.get(product)
    response_for_product.raise_for_status()
    productdetails = response_for_product.json()
    product_id = productdetails["id"]
    # print("Product id",product_id)

    # Retrieve user's choice from the callback query
    choice = query.data

    if choice == "confirm_purchase":
        try:
            # Retrieve product details and total cost from context.user_data
            selected_product = context.user_data.get('selected_product')
            number_of_orders = context.user_data.get('number_of_orders')
            product_currency = context.user_data.get('product_currency')
            total_cost = context.user_data.get('total_cost')

            # Make a request to get user's wallet balance
            get_wallet_balance_endpoint = 'http://127.0.0.1:5000/api/get_balance'
            response = requests.get(get_wallet_balance_endpoint, json={'telegram_id': user_id})
            response_data = response.json()
            available_balance = response_data['available_balance']
            order_quantity = float(number_of_orders) * selected_selling_weight

            if response.status_code == 200:
                to_currency = "BTC"
                total_cost_exchanged = get_currency_conversion(product_currency, to_currency, total_cost)

                if float(available_balance) >= float(total_cost_exchanged):
                    # Make a request to deduct purchase amount from the wallet
                    deduct_wallet_amount_endpoint = 'http://127.0.0.1:5000/api/make_payment'
                    response = requests.post(deduct_wallet_amount_endpoint, json={'telegram_id': user_id, 'amount': total_cost, 'currency': product_currency})

                    if response.status_code == 200:
                        response_data = response.json()
                        transaction_id = response_data['transaction_id']
                        order_endpoint = 'http://127.0.0.1:5000/api/orders'
                        response_order = requests.post(order_endpoint, json={'telegram_id': user_id, 'total_price': total_cost, 'quantity': order_quantity, 'number_of_orders': number_of_orders, 'quantity_unit': selected_selling_weight_measurement, 'product_id': product_id, 'transaction_id': transaction_id})

                        if response_order.status_code == 200:
                            response_data = response_order.json()
                            associated_treasure_data = response_data.get('associated_treasure')
                            # print("Associated_treasure",associated_treasure_data)
                            if isinstance(associated_treasure_data, str) and "No available treasures" in associated_treasure_data:
                                # Fallback message if no available treasure is found
                                context.bot.send_message(chat_id=user_id, text="🎉🛒 Order Confirmed!\n\nThanks for your purchase! We've received your order and are setting sail to find the perfect treasure for you. 🏴‍☠️⛵\n\n💬 Don't worry, we'll keep you posted once we discover your treasure. Your purchase is in good hands. Payment successful. 😊")
                            else:
                                associated_treasure = associated_treasure_data['associated_treasure']

                                if associated_treasure:
                                    treasure_description = associated_treasure['description']
                                    treasure_coordinates = associated_treasure['coordinates']
                                    treasure_image_path = associated_treasure['image_url']

                                    if treasure_image_path:
                                        with open(treasure_image_path, 'rb') as image_file:
                                            img_bytes = BytesIO(image_file.read())
                                            # Send the image in a Telegram message
                                            context.bot.send_photo(chat_id=user_id, photo=img_bytes, caption=f"🎉🛒 Order Confirmed!\n\nGreat news! Your purchase is confirmed. 🏴‍☠️🗺️\n\n📦 Treasure Description: {treasure_description}\n🌍 Coordinates: {treasure_coordinates}\n\n🚚 Your purchase is at {selected_district} as described in the photo!Thanks for choosing us! Payment successful. 😊")
                                            # Clear user_data to start a new order
                                            return ConversationHandler.END
                        else:
                            # Payment failed
                            context.bot.send_message(chat_id=user_id, text=f"Payment failed. Please try again later.")
                            return ConversationHandler.END
                else:
                    # Wallet balance is lower than the payable amount
                    context.bot.send_message(chat_id=user_id, text=f"Your wallet balance ({available_balance}) BTC is insufficient.")
                    context.bot.send_message(chat_id=user_id, text="Do you want to replenish your wallet?")
                    keyboard = [['Yes, I want to replenish'], ['No, cancel the purchase']]
                    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                    context.bot.send_message(chat_id=user_id, text="Please choose an option:", reply_markup=reply_markup)
                    return INSUFFICIENT_BALANCE
            else:
                # Unable to get wallet balance
                context.bot.send_message(chat_id=user_id, text=f"Failed to get wallet balance. Please try again later.")
                return ConversationHandler.END

        except requests.RequestException as e:
            # Handle the error
            context.bot.send_message(chat_id=user_id, text='Failed to process payment. Please try again later.')
            return ConversationHandler.END

    elif choice == "cancel_purchase":
        # Cancel the purchase
        context.bot.send_message(chat_id=user_id, text="Purchase canceled. You can start over anytime.")
        return ConversationHandler.END

    # Go back to the home page after purchase or cancel
    return ConversationHandler.END

def account_details(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username  # Get the Telegram username
    # Get the wallet balance
    get_wallet_balance_endpoint = 'http://127.0.0.1:5000/api/get_balance'
    response = requests.get(get_wallet_balance_endpoint, json={'telegram_id': user_id})
    response_data = response.json()
    available_balance = response_data.get('balance', {}).get('data', {}).get('available_balance', "N/A")
    address = response_data.get('address', "N/A")
    if available_balance:
        # msg = f"Account Details:\nUsername: {username}\nWallet Address: {address}\nAvailable Balance: {available_balance}"
        msg = f"👤 Account Details\n\n"
        msg += f"🔹 Username: {username}\n"
        msg += f"💰 Available Balance: {available_balance}\n"
        msg += f"🏦 Wallet Address: {address}\n"
        context.bot.send_message(chat_id=user_id, text=msg)
    else:
        context.bot.send_message(chat_id=user_id, text="Unable to retrieve wallet balance. Please try again later.")
    return ConversationHandler.END

def insufficient_balance(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat_id
    user_response = update.message.text.lower()
    
    
    if user_response == 'yes, i want to replenish':
        get_wallet_balance_endpoint = 'http://127.0.0.1:5000/api/get_balance'
        response = requests.get(get_wallet_balance_endpoint, json={'telegram_id': user_id})
        response_data = response.json()
        available_balance = response_data.get('balance', {}).get('data', {}).get('available_balance', "N/A")
        address = response_data.get('address', "N/A")

        if address:
            message = f"Please replenish your wallet.\n\nYour Wallet Address: {address}\nAvailable Balance: {available_balance}"
            context.bot.send_message(chat_id=user_id, text=message)
        else:
            context.bot.send_message(chat_id=user_id, text="Unable to retrieve wallet information. Please try again later.")
        return ConversationHandler.END
    elif user_response == 'no, cancel the purchase':
        context.bot.send_message(chat_id=user_id, text="Purchase canceled. You can start over anytime.")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=user_id, text="Invalid option. Please choose an option from the provided buttons.")
        return INSUFFICIENT_BALANCE

def back(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id

    message = "Selection process exited. You can start again any time."
    context.bot.send_message(chat_id=user_id, text=message)

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.message.chat_id

    message = "Selection process canceled. You can start over anytime."
    context.bot.edit_message_text(chat_id=user_id, message_id=query.message.message_id, text=message)

    return ConversationHandler.END

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

def main():
    # Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
    updater = Updater("6449025781:AAGbPmXHfBJjhI18VUhN_F1r7BC7GVyyzC4", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(home,pattern='^home$'))
    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMOJI_VERIFICATION: [CallbackQueryHandler(emoji_verification)],
            HOME: [
                CommandHandler('home', home),
                CallbackQueryHandler(profile, pattern='^profile$'),  
                CallbackQueryHandler(balance, pattern='^balance$'),
                CallbackQueryHandler(last_order, pattern='^last_order$'),
                CallbackQueryHandler(location, pattern='^location$'),
                CallbackQueryHandler(back, pattern='^back$')

            ],
            
            LOCATION: [CallbackQueryHandler(country_selected, pattern='^country-.*$'),
                       CallbackQueryHandler(city_selected, pattern='^city-.*$'),
                       CallbackQueryHandler(cancel, pattern='^🔙$'),
                       CallbackQueryHandler(back, pattern='^back$')],
            DISTRICT: [CallbackQueryHandler(district_selected, pattern='^district-.*$'),
                       CallbackQueryHandler(cancel, pattern='^🔙$'),
                       CallbackQueryHandler(back, pattern='^back$')],
            CATEGORY: [CallbackQueryHandler(category_selected, pattern='^category-.*$'),
                       CallbackQueryHandler(cancel, pattern='^🔙$'),
                       CallbackQueryHandler(back, pattern='^back$')],
            PRODUCT: [CallbackQueryHandler(product_selected, pattern='^product-.*$'),
                      CallbackQueryHandler(back, pattern='^back$'),
                      CallbackQueryHandler(cancel, pattern='^🔙$')],
            GET_QUANTITY: [MessageHandler(Filters.text & ~Filters.command, get_quantity)],
            CONFIRM_PURCHASE: [CallbackQueryHandler(confirm_purchase, pattern='^(confirm_purchase|cancel_purchase)$')],
            DISTRICT_DELIVERY: [CallbackQueryHandler(delivery_district_selected, pattern='^delivery_district-.*$'),
                                CallbackQueryHandler(back, pattern='^back$'),
                                CallbackQueryHandler(cancel, pattern='^🔙$')],
            INSUFFICIENT_BALANCE: [MessageHandler(Filters.text & ~Filters.command, insufficient_balance)],
            ASK_USERNAME: [MessageHandler(Filters.text & ~Filters.command, ask_username)],
            ASK_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, ask_password)],
            # SIGN_IN: [MessageHandler(Filters.text & ~Filters.command, confirm_sign_up)],
            "USERNAME": [MessageHandler(Filters.text & ~Filters.command, ask_password_sign_up)],
            CONFIRM_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, confirm_password)],
            ACCOUNT_DETAILS: [CommandHandler('account', account_details)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        
        
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



