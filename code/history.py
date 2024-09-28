import helper
import logging
import matplotlib.pyplot as plt

def run(message, bot):
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        spend_total_str = ""
        amount = 0.0
        am = ""
        
        # Add all 12 months to the dictionary, including August
        Dict = {
            'Jan': 0.0, 'Feb': 0.0, 'Mar': 0.0, 'Apr': 0.0, 'May': 0.0, 
            'Jun': 0.0, 'Jul': 0.0, 'Aug': 0.0, 'Sep': 0.0, 'Oct': 0.0, 
            'Nov': 0.0, 'Dec': 0.0
        }

        if user_history is None:
            raise Exception("Sorry! No spending records found!")

        # Retrieve user's preferred currency
        preferred_currency = helper.get_user_preferred_currency(chat_id)  # Implement this in helper
        
        spend_total_str = "Here is your spending history (converted to {}): \nDATE, CATEGORY, AMOUNT\n----------------------\n".format(preferred_currency)
        
        if len(user_history) == 0:
            spend_total_str = "Sorry! No spending records found!"
        else:
            for rec in user_history:
                spend_total_str += str(rec) + "\n"
                av = str(rec).split(",")
                ax = av[0].split("-")
                am = ax[1]  # Extract month from date

                amount = float(av[2])
                currency = av[3].strip() if len(av) > 3 else 'USD'  # Get the currency from the record if available, default to USD

                # Convert the amount to the user's preferred currency
                converted_amount = helper.convert_currency(amount, currency, preferred_currency)
                
                # Safely update the Dict using .get() to avoid KeyError
                Dict[am] = Dict.get(am, 0.0) + converted_amount

        bot.send_message(chat_id, spend_total_str)

        # Generate and send the spending histogram as a bar chart
        plt.clf()  # Clear any existing plot
        width = 1.0
        plt.bar(Dict.keys(), Dict.values(), width, color='g')
        plt.savefig('histo.png')
        bot.send_photo(chat_id, photo=open('histo.png', 'rb'))

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))

