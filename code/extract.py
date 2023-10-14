import helper
import logging
from telegram import InputFile
from telebot import types

# The main funtion of category.py.
# User can start to manage their categories after calling it
def run(message, bot):
    # Send "Hello, World!"
    bot.send_message(message.chat.id, "Hello, World!")

    try:
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        file_path = 'code/sample.csv'

        """
        TODO
        1. Convert user_history to csv
        2. Think about separating attributes from the string
        3. Delete file from local after sending
        """
    

        # Send the file to the user
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, document=file)
    except Exception as e:
        logging.error(str(e))
