import helper
import logging
from telebot import types


def run(message, bot):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Running estimate calculation...")  # Ensure this message is sent
    history = helper.getUserHistory(chat_id)
    
    if not history:
        bot.send_message(chat_id, "No spending data available!")
        return
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        options = helper.getSpendEstimateOptions()
        for option in options:
            markup.add(option)
        msg = bot.reply_to(message, "Select an option for estimate calculation", reply_markup=markup)
        bot.register_next_step_handler(msg, estimate_total, bot)


def estimate_total(message, bot):
    chat_id = message.chat.id
    selected_option = message.text
    
    try:
        # Validate option
        if selected_option not in helper.getSpendEstimateOptions():
            raise ValueError("Invalid option")
        
        bot.send_message(chat_id, "Calculating estimate for {}".format(selected_option))
        
        # Mock some estimate calculation here
        estimate = 1000  # Dummy estimate value
        
        bot.send_message(chat_id, "Your estimated spending for {} is: ${}".format(selected_option, estimate))
    
    except Exception as e:
        bot.send_message(chat_id, "Error: {}".format(str(e)))
        logging.exception("Failed to calculate estimate: {}".format(e))

