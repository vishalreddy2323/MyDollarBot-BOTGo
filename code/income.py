import re
import helper

# Conversion rates can be modified based on the requirements
conversion_rates = {
    'USD': 1.0,  # Base currency
    'INR': 0.012,  # Example conversion rate to USD
    'EUR': 1.1,   # Example conversion rate to USD
}

# income.py


# Set the user's income
def set_income(message, bot):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Please enter your monthly income:")

# Process income input
def process_income_input(message, bot):
    chat_id = message.chat.id
    income_value = float(message.text)

    # Store the income in user data
    helper.setUserIncome(chat_id, income_value)
    bot.send_message(chat_id, f"Your monthly income has been set to ${income_value}.")

# Check if the transaction exceeds the user's set income
def check_transaction_limit(chat_id, amount, bot):
    # Retrieve user's income and expenditure from helper functions
    user_data = helper.getUserData(chat_id)

    # Check if income has been set
    if 'income' not in user_data or user_data['income'] == 0:
        bot.send_message(chat_id, "You haven't set your monthly income yet. Please use /income to set your income.")
        return True  # Stop further transaction process

    total_expenditure = helper.calculate_total_expenditure(chat_id)

    # Check if the new transaction will exceed the income
    if total_expenditure + amount > user_data['income']:
        bot.send_message(chat_id, f"Transaction cannot be recorded! Your total expenditure of ${total_expenditure + amount} exceeds your monthly income of ${user_data['income']}. Please update your income or hold off on new transactions.")
        return True  # Stop further transaction process

    return False  # Allow the transaction if income limit is not exceeded

