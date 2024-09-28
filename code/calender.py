from datetime import datetime
import helper  # Assuming you have helper functions in helper.py
from telebot import TeleBot

# Initialize the bot with your token (Replace YOUR_BOT_API_KEY with the actual bot token)
bot = TeleBot("YOUR_BOT_API_KEY")  # Replace with your bot token

# Dictionary to track the user sessions
user_sessions = {}  # Tracks if the user is waiting for date input

# Add the /calendar command to ask for a date
@bot.message_handler(commands=['calendar'])
def send_calendar(message):
    bot.send_message(message.chat.id, "Please select a date (format: YYYY-MM-DD):")
    user_sessions[message.chat.id] = 'waiting_for_date'  # Track that this user is selecting a date

# Capture the user input for the date and retrieve transactions
@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id) == 'waiting_for_date')
def capture_date_input(message):
    try:
        # Validate and convert the message into a datetime object
        selected_date = datetime.strptime(message.text.strip(), '%Y-%m-%d')
        bot.send_message(message.chat.id, f"Date {selected_date.date()} selected. Retrieving transactions...")
        show_spend_for_date(selected_date, message.chat.id)
        # Once the date is processed, remove the user session
        user_sessions.pop(message.chat.id, None)
    except ValueError:
        bot.send_message(message.chat.id, "Invalid date format! Please use YYYY-MM-DD.")

# Function to filter and display transactions for a specific date
def show_spend_for_date(selected_date, chat_id):
    transactions = helper.getUserHistory(chat_id)  # Assuming this function returns all transactions for the user
    filtered_transactions = []

    # Filter transactions for the selected date
    for txn in transactions:
        txn_date = datetime.strptime(txn['date'], '%Y-%m-%d')  # Assuming transactions have a 'date' field
        if txn_date.date() == selected_date.date():
            filtered_transactions.append(txn)

    # Send the filtered transactions to the user
    if filtered_transactions:
        for txn in filtered_transactions:
            bot.send_message(chat_id, f"{txn['date']} - {txn['category']}: ${txn['amount']}")
    else:
        bot.send_message(chat_id, "No transactions found for the selected date.")

# If this script is the main entry point, start polling the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)

