import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
import requests
from telegram import InputFile
import os
# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Conversation states
EMOJI_VERIFICATION = range(4)
ASK_USERNAME ,AUTHENTICATED,ASK_PASSWORD ,HOME= range(4)
emojis = ['👍', '👌', '😊', '🎉', '🍕', '🌟', '🐢', '🌈', '🎵', '🚀', '🍦', '🐳', '🏀', '🌺', '📚', '🍔']
def start(update: Update, context: CallbackContext) -> int:
    # Emojis for verification
    verification_emoji = random.choice(emojis)
    context.user_data['verification_emoji'] = verification_emoji
    context.user_data['attempts_left'] = 3  # Reset attempts count

    # Arrange emojis in rows with three buttons per row
    emoji_buttons = [
        [InlineKeyboardButton(emoji, callback_data=emoji) for emoji in emojis[i:i+3]]
        for i in range(0, len(emojis), 3)
    ]
    # Add "Cancel" and "Back" buttons to the keyboard
    emoji_buttons.append([InlineKeyboardButton("Cancel", callback_data="❌"), InlineKeyboardButton("Back", callback_data="🔙")])

    reply_markup = InlineKeyboardMarkup(emoji_buttons)
    update.message.reply_text(f"Please select one emoji to verify that you are not a bot:\n({verification_emoji} will verify you)", reply_markup=reply_markup)
    return EMOJI_VERIFICATION

def emoji_verification(update: Update, context: CallbackContext) -> int:
    user_choice = update.callback_query.data
    verification_emoji = context.user_data['verification_emoji']
    update.callback_query.answer()  # Acknowledge the button press

    # Check if the user selected the correct emoji
    if user_choice == verification_emoji:
        update.callback_query.message.reply_text(f"Great choice! You selected {user_choice}. You are verified.")
        reset_verification_data(context)
        context.bot.send_message(chat_id=update.effective_user.id, text="Please provide your courier username:")
        return ASK_USERNAME
    else:
        # Decrement the attempts left
        if 'attempts_left' not in context.user_data:
            context.user_data['attempts_left'] = 3
        context.user_data['attempts_left'] -= 1

        if context.user_data['attempts_left'] <= 0:
            update.callback_query.message.reply_text("Verification failed. You have been locked out. Please contact Admin for your verification.")
            reset_verification_data(context)
            return start(update, context)
        else:
            update.callback_query.message.reply_text(f"Incorrect emoji selected. Please try again. ({context.user_data['attempts_left']} attempts left.")

            # Remove the selected emoji from the list
            emojis.remove(user_choice)

            # Show the keyboard with remaining attempts and the emoji to select
            emoji_buttons = [
                [InlineKeyboardButton(emoji, callback_data=emoji) for emoji in emojis[i:i + 3]]
                for i in range(0, len(emojis), 3)
            ]
            reply_markup = InlineKeyboardMarkup(emoji_buttons)
            update.callback_query.message.reply_text(f"Please select {verification_emoji} to verify that you are not a bot:", reply_markup=reply_markup)

            return EMOJI_VERIFICATION

def check_username(update: Update, context: CallbackContext) -> int:
    context.user_data['username'] = update.message.text
    update.message.reply_text("Please provide your courier password:")
    return ASK_PASSWORD

def check_password(update: Update, context: CallbackContext) -> int:
    password = update.message.text
    username = context.user_data.get('username')

    data = {
        'username': username,
        'password': password
    }

    # Make a POST request to your authentication endpoint
    response = requests.post('http://127.0.0.1:5000/api/authenticate', json=data)
    
    if response.status_code == 200:
        courier_data = response.json().get('courier')
        context.user_data['authenticated_courier'] = courier_data
        context.user_data['state'] = AUTHENTICATED
        # Fetch tasks for the authenticated courier
        tasks_response = requests.get(f'http://127.0.0.1:5000/api/couriers/{courier_data["id"]}/pending-tasks')
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            context.user_data['tasks'] = tasks
            # print(tasks)
        update.message.reply_text("Username and password verified. Welcome to the home page!")
        return home(update,context)
    else:
        update.message.reply_text("Invalid username or password. Please try again. start by using /start command ")
        return check_username(update, context)

def reset_verification_data(context: CallbackContext):
    # Reset verification data
    if 'verification_emoji' in context.user_data:
        del context.user_data['verification_emoji']
    if 'attempts_left' in context.user_data:
        del context.user_data['attempts_left']

def home(update: Update, context: CallbackContext):
    if 'state' not in context.user_data or context.user_data['state'] != AUTHENTICATED:
        update.message.reply_text("You need to log in first to access this feature.")
        return start(update, context)
    # Define buttons for "Tasks" and "Statistics"
    keyboard = [[InlineKeyboardButton("Tasks", callback_data="tasks"), InlineKeyboardButton("Statistics", callback_data="statistics")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the Home Page! Choose an option:", reply_markup=reply_markup)
    return HOME 

def list_tasks(update: Update, context: CallbackContext):
    tasks_data = context.user_data.get('tasks', [])

    if not tasks_data:
        update.callback_query.message.reply_text("You don't have any pending tasks.")
        return HOME  # Go back to the home state

    keyboard = [
        [InlineKeyboardButton(task['name'], callback_data=f"task_{task['id']}")]
        for task in tasks_data
    ]
    keyboard.append([InlineKeyboardButton("Back to Home", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Your Pending Tasks:", reply_markup=reply_markup)
    return "list_tasks"  # Go back to the home state

def task_selected(update: Update, context: CallbackContext):
    task_id = int(update.callback_query.data.split('_')[1])
    context.user_data["selected_task_id"] = task_id

    courier_data = context.user_data.get("authenticated_courier")
    context.user_data["courier_data_1"]=courier_data
    courier_id = courier_data["id"]

    task_data = fetch_task_data_from_endpoint(courier_id, task_id)  # Pass courier_id and task_id

    task_info = (
        f"📋 Task #{task_data['id']}:\n"
        f"📌 Name: {task_data['name']}\n"
        f"🏁 Status: {task_data['status']}\n"
        f"📍 Address: {task_data['address']}\n"
        f"🌐 Area of Distribution: {task_data['area_of_distribution']}\n"
        f"💰 Commission: {task_data['commission']} {task_data['commission_currency']}\n"
        f"💲 Cost of Item: {task_data['cost_of_item']} {task_data['commission_currency']}\n"
        f"📦 Number of Items: {task_data['number_of_items']}\n"
        f"🎁 Number of Treasures: {task_data['number_of_treasures']}\n"
        f"⚖️ Item Weight: {task_data['weight_of_item']} {task_data['item_weight_measurement']}"
    )


    context.user_data["treasures"] = []
    context.user_data["current_treasures"] = 1

    keyboard = [
        [InlineKeyboardButton("Submit Solution", callback_data="submit_solution")],
        [InlineKeyboardButton("Back to Tasks", callback_data="tasks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(task_info, reply_markup=reply_markup)
    # update.callback_query.message.reply_text("Submit your solutions one by one. You can stop anytime by typing /stop.")
    return "task_selected"

def submit_solution(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    current_solution = context.user_data.get("current_treasures", 1)
    
    selected_task_id = context.user_data.get("selected_task_id")
    courier_data = context.user_data.get("courier_data_1")  # Assuming you store the courier ID in context.user_data
    print("Current solution,selected_Task_id", current_solution, selected_task_id)
    courier_id = courier_data["id"]
    task_data = fetch_task_data_from_endpoint(courier_id, selected_task_id)  # Fetch task data using courier_id and task_id
  
    total_treasures = task_data.get("number_of_treasures", 0)
    context.user_data["total_treasures"]=total_treasures
    print("total treasures", total_treasures)
    if current_solution > total_treasures:
        # All solutions for the task have been submitted
        context.bot.send_message(chat_id=user_id, text="All solutions for this task have been submitted. Use /home to return to the main menu.")
        return ConversationHandler.END

    context.bot.send_message(chat_id=user_id, text=f"Solution #{current_solution} for Task #{selected_task_id}:")

    # Expecting description
    context.bot.send_message(chat_id=user_id, text="🗺️ Please provide a description for the solution.\nExample: Hidden under the big oak tree near the fountain.")

    return "solution_description"

def fetch_task_data_from_endpoint(courier_id, task_id):
    url = f"http://127.0.0.1:5000/api/couriers/{courier_id}/tasks/{task_id}"  # Replace with your actual endpoint URL
    response = requests.get(url)

    if response.status_code == 200:
        task_data = response.json()
        return task_data
    else:
        return None

def receive_solution_description(update: Update, context: CallbackContext):
    description = update.message.text
    context.user_data["treasures"].append({"description": description})
    update.message.reply_text("🌍 Please provide the coordinates (latitude,longitude) for the solution.\nExample: 40.7128,-74.0060")
    return "solution_coordinates"

def receive_solution_coordinates(update: Update, context: CallbackContext):
    coordinates = update.message.text
    context.user_data["treasures"][-1]["coordinates"] = coordinates
    update.message.reply_text("📷 Please upload a photo for the treasure:")
    return "solution_photo"

def receive_solution_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]  # Get the photo object
    photo_id = photo.file_id

    # Download the photo and save it to the "uploads" folder
    file = context.bot.get_file(photo_id)
    file.download(os.path.join("uploads", f"{photo_id}.jpg"))

    current_solution = context.user_data.get("current_treasures", 1)
    selected_task_id = context.user_data.get("selected_task_id")
    description = context.user_data["treasures"][-1]["description"]
    coordinates = context.user_data["treasures"][-1]["coordinates"]
    photo_url = f"uploads/{photo_id}.jpg"

    # Sending the solution data to your endpoint
    response = send_treasure(selected_task_id, current_solution, description, coordinates, photo_url)
    if response == "success":
        context.user_data["treasures"][-1]["photo_url"] = photo_url
        context.user_data["current_treasures"] += 1

        total_treasures =  context.user_data.get("total_treasures")
        treasures_left = total_treasures - current_solution

        reply_text = (
        f"🎉 Received Treasure Data 🎉\n"
        f"Description: {description}\n"
        f"Coordinates: {coordinates}\n"
        f"🏆 You've submitted Treasure for Task #{selected_task_id}.\n"
        f"🔍 You still have {treasures_left} treasures to discover!"
        )

        
        # Send the image along with the reply text
        with open(photo_url, "rb") as photo_file:
            update.message.reply_photo(photo=InputFile(photo_file), caption=reply_text)

        return HOME
    else:
        msg = "Oops! Something went wrong while submitting the treasure."
        update.message.reply_text(msg)
        return HOME

def send_treasure(task_id, solution_number, description, coordinates, photo_url):
    # Prepare the data to be sent to your endpoint
    treasure_data = {
        "task_id": task_id,
        "solution_number": solution_number,
        "description": description,
        "coordinates": coordinates,
        "image_url": photo_url
    }

    # Make a POST request to your endpoint to send the treasure data
    response = requests.post('http://127.0.0.1:5000/api/treasures', json=treasure_data)
    
    if response.status_code == 201:
        print("Treasure data sent successfully!")
        return "success"
    else:
        print("Failed to send treasure data.")
        return "error"

def stop_solution_submission(update: Update, context: CallbackContext):
    update.message.reply_text("Solution submission stopped. Use /start to return to the main menu.")
    return ConversationHandler.END

def statistics(update: Update, context: CallbackContext):
    selected_courier_id = context.user_data.get("authenticated_courier")
    # Fetch statistics for the courier's earnings over time
    statistics_data = fetch_statistics_from_endpoint(selected_courier_id["id"])

    if not statistics_data:
        update.callback_query.message.reply_text("📊 No statistics available.")
    else:
        statistics_info = "\n".join([f"📈 {key}: {value}" for key, value in statistics_data.items()])
        update.callback_query.message.reply_text("📊 Your Earnings Statistics:\n" + statistics_info +" usd")

def fetch_statistics_from_endpoint(courier_id):
    url = f"http://127.0.0.1:5000/api/couriers/{courier_id}/earnings"  # Replace with your actual endpoint URL
    response = requests.get(url)

    if response.status_code == 200:
        statistics_data = response.json()
        return statistics_data
    else:
        return None

def get_courier_bot_token():
    try:
        response = requests.get('http://127.0.0.1:5000/api/latest/courier_bot')
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print('Failed to fetch Reviews Bot token:', response.status_code)
    except Exception as e:
        print('Error:', e)
    return None

def main():
    # Add handlers for the conversation states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMOJI_VERIFICATION: [CallbackQueryHandler(emoji_verification)],
            ASK_USERNAME: [MessageHandler(Filters.text & ~Filters.command, check_username)],
            ASK_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, check_password)],
            HOME: [
                CommandHandler('home', home),
                CallbackQueryHandler(list_tasks, pattern='^tasks$'),  
                CallbackQueryHandler(statistics, pattern='^statistics$'),
            ],
             "list_tasks": [CallbackQueryHandler(task_selected, pattern='^task_')],
            "task_selected": [CallbackQueryHandler(submit_solution, pattern='^submit_solution$')],
             "solution_description":[ MessageHandler(Filters.text & ~Filters.command, receive_solution_description)],
             "solution_coordinates":[MessageHandler(Filters.text & ~Filters.command, receive_solution_coordinates)],
             "solution_photo":[MessageHandler(Filters.photo & ~Filters.command, receive_solution_photo)],
            # "submit_another_solution":[MessageHandler(Filters.text & ~Filters.command,confirm_submit_another)],
        },
        fallbacks=[CommandHandler('stop', stop_solution_submission)],
        per_user=True,
        allow_reentry=True
    )
    courier_bot = get_courier_bot_token()
    # Create the updater, add handlers, and start the bot
    updater = Updater(token=courier_bot, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

