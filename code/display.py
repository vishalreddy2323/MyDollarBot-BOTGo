import time
import os
import helper
import graphing
import logging
from telebot import types
from datetime import datetime

def show_expense_summary(bot, chat_id, expenses, selected_category):
    """Display a summary of expenses in the user's preferred currency."""
    preferred_currency = helper.get_user_preferred_currency(chat_id)
    total_amount = 0

    # Sum expenses in the preferred currency
    for expense in expenses:
        amount = expense['amount']
        currency = expense['currency']
        total_amount += helper.convert_currency(amount, currency, preferred_currency)

    if selected_category == 'All':
        bot.send_message(chat_id, f"Your total expenses across all categories are {total_amount:.2f} {preferred_currency}.")
    else:
        bot.send_message(chat_id, f"Your total expenses in {selected_category} are {total_amount:.2f} {preferred_currency}.")

def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)

    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2

        # Add categories to the markup, including "All"
        for category in helper.getSpendCategories():
            markup.add(category)
        markup.add('All')  # Add 'All' category to see expenses across all categories
        msg = bot.reply_to(message, 'Please select a category to see details', reply_markup=markup)
        bot.register_next_step_handler(msg, select_period, bot)

def select_period(message, bot):
    """Ask user to select day or month after they choose a category."""
    chat_id = message.chat.id
    selected_category = message.text

    # Store the selected category temporarily
    bot.send_message(chat_id, f"You selected {selected_category}. Now please select a time period (Day or Month).")

    # Create a markup for Day/Month selection
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add('Day', 'Month')

    # Move to the next step
    msg = bot.reply_to(message, 'Please select a period to see the spending details.', reply_markup=markup)
    bot.register_next_step_handler(msg, display_total, bot, selected_category)


def display_total(message, bot, selected_category):
    global total
    global bud
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception(f"Sorry I can't show spendings for \"{DayWeekMonth}\"!")

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(0.5)

        # Get user preferred currency
        preferred_currency = helper.get_user_preferred_currency(chat_id)

        # Filter the expenses based on the selected time period (Day or Month) and category
        queryResult = []
        if DayWeekMonth == 'Day':
            query = datetime.now().today().strftime(helper.getDateFormat())
            if selected_category == 'All':
                queryResult = [value for index, value in enumerate(history) if str(query) in value]
            else:
                queryResult = [value for index, value in enumerate(history) if str(query) in value and selected_category in value]
        elif DayWeekMonth == 'Month':
            query = datetime.now().today().strftime(helper.getMonthFormat())
            if selected_category == 'All':
                queryResult = [value for index, value in enumerate(history) if str(query) in value]
            else:
                queryResult = [value for index, value in enumerate(history) if str(query) in value and selected_category in value]

        # Check if there are no expenses in this category or all categories
        if not queryResult:
            if selected_category == 'All':
                remaining_budget = helper.getOverallRemainingBudget(chat_id)  # Get overall remaining budget for all categories
                bot.send_message(chat_id, f"No expenses recorded for all categories in {DayWeekMonth}. Remaining Amount: ${remaining_budget:.2f} (Income - Expenditure)")
            else:
                remaining_budget = helper.get_remaining_budget(chat_id, selected_category)
                bot.send_message(chat_id, f"No expenses recorded for {selected_category} in {DayWeekMonth}. Remaining Amount: ${remaining_budget:.2f} (Income - Expenditure)")
        else:
            # Calculate total spending in the category or all categories
            total_text = calculate_spendings(queryResult, preferred_currency)
            total = total_text

            if selected_category != 'All':
                bud = helper.getCategoryBudgetByCategory(chat_id, selected_category)
            else:
                bud = helper.getOverallBudget(chat_id)  # Get overall budget for all categories

            spending_text = f"Here are your total spendings for {selected_category} in {DayWeekMonth.lower()}:\nCATEGORIES, AMOUNT \n----------------------\n{total_text}"
            bot.send_message(chat_id, spending_text)

            # Show remaining balance
            if selected_category == 'All':
                 remaining_budget = helper.get_remaining_budget(chat_id, selected_category)
            else:
                remaining_budget = helper.get_remaining_budget(chat_id, 'All')

            bot.send_message(chat_id, f"Remaining Amount: ${remaining_budget:.2f}")

            # Ask the user if they want to see a plot
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            for plot in helper.getplot():
                markup.add(plot)
            msg = bot.reply_to(message, 'Please select a plot to see the total expense', reply_markup=markup)
            bot.register_next_step_handler(msg, plot_total, bot)

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))


def plot_total(message, bot):
    chat_id = message.chat.id
    pyi = message.text
    if pyi == 'Bar with budget':
        graphing.visualize(total, bud)
        bot.send_photo(chat_id, photo=open('expenditure.png', 'rb'))
        os.remove('expenditure.png')
    elif pyi == 'Bar without budget':
        graphing.viz(total)
        bot.send_photo(chat_id, photo=open('expend.png', 'rb'))
        os.remove('expend.png')
    else:
        graphing.vis(total)
        bot.send_photo(chat_id, photo=open('pie.png', 'rb'))
        os.remove('pie.png')

def calculate_spendings(queryResult, preferred_currency):
    total_dict = {}

    for row in queryResult:
        s = row.split(',')
        cat = s[1]  # Category
        amount = float(s[2])
        currency = s[3]  # Currency of the expense

        # Convert to preferred currency
        converted_amount = helper.convert_currency(amount, currency, preferred_currency)

        # Add the expense to the total for the category
        if cat in total_dict:
            total_dict[cat] = round(total_dict[cat] + converted_amount, 2)
        else:
            total_dict[cat] = converted_amount

    total_text = ""
    for key, value in total_dict.items():
        total_text += f"{key} {value:.2f} {preferred_currency}\n"

    return total_text

