import helper
import logging
from telebot import types, telebot
from datetime import datetime
from jproperties import Properties
import requests
import os

option = {}

configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

api_token = str(configs.get('api_token').data)

bot = telebot.TeleBot(api_token)

if not os.path.exists("receipts"):
    os.makedirs("receipts")


def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, 'Invalid category selected.',
                             reply_markup=types.ReplyKeyboardRemove())
            raise Exception(f"Sorry I don't recognize this category \"{selected_category}\"!")

        option[chat_id] = selected_category
        msg = bot.send_message(
            chat_id, f'How much did you spend on {selected_category}? (Enter numeric values only)')
        bot.register_next_step_handler(
            msg, post_amount_input, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = helper.get_help_text()
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)

def post_amount_input(message, bot, selected_category):
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        # Retrieve user data or create an empty dictionary if none exists
        user_data = helper.getUserData(chat_id) or {}

        # Check if user has set an income
        if 'income' not in user_data or user_data['income'] == 0:
            bot.send_message(chat_id, "You haven't set an income yet. Please use /income to set your monthly income.")
            return

        # Check if transaction exceeds income
        if helper.checkIfExceedsIncome(chat_id, float(amount_value), bot):
            return  # If income limit is exceeded, stop further processing

        # Ask for the date of the transaction
        msg = bot.send_message(chat_id, 'Please enter the date of this transaction (format: YYYY-MM-DD):')
        bot.register_next_step_handler(msg, process_transaction_date, bot, amount_value, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))


def process_transaction_date(message, bot, amount_value, selected_category):
    try:
        chat_id = message.chat.id
        date_text = message.text
        try:
            # Validate and parse the entered date
            selected_date = datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            bot.send_message(chat_id, "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Store the transaction details with the selected date
        date_of_entry = selected_date.strftime(helper.getDateFormat())
        helper.write_json(add_user_record(
            chat_id, f"{date_of_entry},{selected_category},{amount_value}"))

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row(types.KeyboardButton("Yes, upload receipt"))
        markup.row(types.KeyboardButton("No, I'm done"))
        msg = bot.send_message(
            chat_id, 'Do you want to upload a receipt image (if available)?', reply_markup=markup)
        bot.register_next_step_handler(
            msg, handle_receipt_decision, bot, amount_value, selected_category, date_of_entry)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))


def handle_receipt_decision(message, bot, amount_value, selected_category, date_of_entry):
    try:
        chat_id = message.chat.id
        decision = message.text.lower()

        if decision == "yes, upload receipt":
            bot.send_message(chat_id, 'Please upload a receipt image.')
            bot.register_next_step_handler(message, handle_uploaded_receipt, bot)
        elif decision == "no, i'm done":
            bot.send_message(chat_id, 'The expenditure is recorded!')
            helper.display_remaining_budget(message, bot, selected_category)
        else:
            bot.send_message(chat_id, 'Invalid choice. Please select "Yes, upload receipt" or "No, I\'m done".')
            markup = types.ReplyKeyboardRemove()
            msg = bot.send_message(chat_id, 'Do you want to upload a receipt image (if available)?', reply_markup=markup)
            bot.register_next_step_handler(msg, handle_receipt_decision, bot, amount_value, selected_category, date_of_entry)
    except Exception as e:
        logging.exception(str(e))
        bot.send_message(chat_id, 'Error occurred while handling receipt decision.')


def add_user_record(chat_id, record_to_be_added):
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]['data'].append(record_to_be_added)
    return user_list

