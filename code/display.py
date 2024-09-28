import time
import os
import helper
import graphing
import logging
from telebot import types
from datetime import datetime

def show_expense_summary(bot, chat_id, expenses):
    """Display a summary of expenses in the user's preferred currency."""
    preferred_currency = helper.get_user_preferred_currency(chat_id)
    total_amount = 0

    # Sum expenses in the preferred currency
    for expense in expenses:
        amount = expense['amount']
        currency = expense['currency']
        total_amount += helper.convert_currency(amount, currency, preferred_currency)

    bot.send_message(chat_id, f"Your total expenses are {total_amount:.2f} {preferred_currency}.")

def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in helper.getSpendDisplayOptions():
            markup.add(mode)
        msg = bot.reply_to(message, 'Please select a category to see details', reply_markup=markup)
        bot.register_next_step_handler(msg, display_total, bot)

total = ""
bud = ""

def display_total(message, bot):
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
        total_text = ""

        # Get user preferred currency
        preferred_currency = helper.get_user_preferred_currency(chat_id)

        # Get budget data for each category
        budgetData = {}
        if helper.isOverallBudgetAvailable(chat_id):
            budgetData = helper.getOverallBudget(chat_id)
        else:
            categories = helper.getSpendCategories()
            for category in categories:
                if helper.isCategoryBudgetByCategoryAvailable(chat_id, category):
                    budgetData[category] = helper.getCategoryBudgetByCategory(chat_id, category)

        # Filter the expenses based on the selected time period (Day or Month)
        if DayWeekMonth == 'Day':
            query = datetime.now().today().strftime(helper.getDateFormat())
            queryResult = [value for index, value in enumerate(history) if str(query) in value]
        elif DayWeekMonth == 'Month':
            query = datetime.now().today().strftime(helper.getMonthFormat())
            queryResult = [value for index, value in enumerate(history) if str(query) in value]

        total_text = calculate_spendings(queryResult, preferred_currency)
        total = total_text
        bud = budgetData
        spending_text = display_budget_by_text(history, budgetData, preferred_currency)

        if len(total_text) == 0:
            spending_text += f"----------------------\nYou have no spendings for {DayWeekMonth}!"
            bot.send_message(chat_id, spending_text)
        else:
            spending_text += f"\n----------------------\nHere are your total spendings {DayWeekMonth.lower()}:\nCATEGORIES, AMOUNT \n----------------------\n{total_text}"
            bot.send_message(chat_id, spending_text)
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
        cat = s[1]
        amount = float(s[2])
        currency = s[3]

        # Convert to preferred currency
        converted_amount = helper.convert_currency(amount, currency, preferred_currency)

        if cat in total_dict:
            total_dict[cat] = round(total_dict[cat] + converted_amount, 2)
        else:
            total_dict[cat] = converted_amount

    total_text = ""
    for key, value in total_dict.items():
        total_text += f"{key} {value:.2f} {preferred_currency}\n"
    return total_text

def display_budget_by_text(history, budget_data, preferred_currency) -> str:
    query = datetime.now().today().strftime(helper.getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]
    total_text = calculate_spendings(queryResult, preferred_currency)
    budget_display = ""
    total_text_split = [line for line in total_text.split('\n') if line.strip() != '']

    if isinstance(budget_data, str):
        # Overall budget
        budget_val = float(budget_data)
        total_expense = sum(float(expense.split(' ')[1]) for expense in total_text_split)
        remaining = budget_val - total_expense
        budget_display += f"Overall Budget is: {budget_val}\n----------------------\nCurrent remaining budget is {remaining:.2f}\n"
    elif isinstance(budget_data, dict):
        budget_display += "Budget by Categories:\n"
        categ_remaining = {key: float(val) for key, val in budget_data.items()}
        for i in total_text_split:
            a = i.split(' ')
            category, expense_amount = a[0], float(a[1])
            categ_remaining[category] = categ_remaining.get(category, 0) - expense_amount
        budget_display += "----------------------\nCurrent remaining budget is: \n"
        for key, val in categ_remaining.items():
            budget_display += f"{key}: {val:.2f}\n"
    return budget_display

