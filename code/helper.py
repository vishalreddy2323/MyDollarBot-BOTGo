import re
import json
import os
from datetime import datetime

choices = ['Date', 'Category', 'Cost']
plot = ['Bar with budget', 'Pie', 'Bar without budget']
spend_display_option = ['Day', 'Month']
spend_categories = ['Food', 'Groceries', 'Utilities',
                    'Transport', 'Shopping', 'Miscellaneous']
spend_estimate_option = ['Next day', 'Next month']
update_options = {
    'continue': 'Continue',
    'exit': 'Exit'
}

budget_options = {
    'update': 'Add/Update',
    'view': 'View',
    'max_spend': 'Transaction Max Spend Limit',
    'delete': 'Delete'
}

budget_types = {
    'overall': 'Overall Budget',
    'category': 'Category-Wise Budget',
}

data_format = {
    'data': [],
    'budget': {
        'overall': None,
        'category': None,
        'max_per_txn_spend': None
    }
}

category_options = {
    'add': 'Add',
    'delete': 'Delete',
    'view': 'Show Categories'
}

# set of implemented commands and their description
commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'calendar': 'View transactions for a selected date',
    'add_recurring': 'Add a new recurring expense for future months',
    'display': 'Show sum of expenditure for the current day/month',
    'estimate': 'Show an estimate of expenditure for the next day/month',
    'history': 'Display spending history',
    'delete': 'Clear/Erase all your records',
    'edit': 'Edit/Change spending details',
    'budget': 'Add/Update/View/Delete budget',
    'category': 'Add/Delete/Show custom categories',
    'extract': 'Extract data into CSV',
    'sendEmail': 'Email CSV to user',
    'receipt': 'Show the receipt for the day',
    'income': 'Add income for the month'
}

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

# function to load .json expense record data
def read_json():
    try:
        if not os.path.exists('expense_record.json'):
            with open('expense_record.json', 'w') as json_file:
                json_file.write('{}')
            return {}
        elif os.stat('expense_record.json').st_size != 0:
            with open('expense_record.json') as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data
        else:
            return {}  # Return an empty dictionary if file is empty
    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        return {}  # Return an empty dictionary in case of any errors

def write_json(user_list):
    try:
        with open('expense_record.json', 'w') as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Sorry, the data file could not be found.')

def validate_entered_amount(amount_entered):
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match("^[1-9][0-9]{0,14}$", amount_entered):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0

def validate_entered_duration(duration_entered):
    if duration_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}", duration_entered):
        duration = int(duration_entered)
        if duration > 0:
            return str(duration)
    return 0


# In helper.py
def get_help_text():
    return "Here is some help text"


# Stores the user's income in a JSON file or in-memory data structure
def setUserIncome(chat_id, income_value):
    user_list = read_json()
    
    # Ensure that user_list is not None and create an empty user data if necessary
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = createNewUserRecord()

    user_list[str(chat_id)]['income'] = income_value
    write_json(user_list)

# Retrieves user data including income and transactions
def getUserData(chat_id):
    # Implement logic to retrieve user data from storage (e.g., JSON or database)
    user_data = read_json()
    if str(chat_id) in user_data:
        return user_data[str(chat_id)]
    else:
        return {}

# Calculate total expenditure for the current month
def calculate_total_expenditure(chat_id):
    transactions = getTransactionsForChat(chat_id)
    total_expenditure = 0.0

    # Sum up all transactions for the month
    for txn in transactions:
        txn_amount = float(txn.split(',')[2])  # Assuming amount is the third value in the transaction string
        total_expenditure += txn_amount

    return total_expenditure


def validate_transaction_limit(chat_id, amount_value, bot):
    if isMaxTransactionLimitAvailable(chat_id):
        maxLimit = round(float(getMaxTransactionLimit(chat_id)), 2)
        if round(float(amount_value), 2) >= maxLimit:
            bot.send_message(
                chat_id, 'Warning! You went over your transaction spend limit')

def getUserHistory(chat_id):
    data = getUserData(chat_id)
    if data is not None:
        return data['data']
    return None

def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if (str(chat_id) in user_list):
        return user_list[str(chat_id)]
    return None

def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, 'Oh no! ' + str(e))

def createNewUserRecord():
    return data_format

def getOverallBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['overall']

def getCategoryBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['category']

def getMaxTransactionLimit(chatId):
    data = getUserData(chatId)
    if data is None or 'budget' not in data or 'max_per_txn_spend' not in data['budget']:
        return None
    return data['budget']['max_per_txn_spend']

def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]

def canAddBudget(chatId):
    return (getOverallBudget(chatId) is None) and (getCategoryBudget(chatId) is None)

def isOverallBudgetAvailable(chatId):
    return getOverallBudget(chatId) is not None

def isCategoryBudgetAvailable(chatId):
    return getCategoryBudget(chatId) is not None

def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None:
        return False
    return cat in data.keys()

def isMaxTransactionLimitAvailable(chatId):
    return getMaxTransactionLimit(chatId) is not None

def display_remaining_budget(message, bot, cat):
    chat_id = message.chat.id
    if isOverallBudgetAvailable(chat_id):
        display_remaining_overall_budget(message, bot)
    elif isCategoryBudgetByCategoryAvailable(chat_id, cat):
        display_remaining_category_budget(message, bot, cat)

def getTransactionsForChat(chat_id):
    """
    This function retrieves the list of transactions for the specified user (chat_id).
    Modify it according to your data structure (e.g., stored JSON, database, etc.).
    """
    user_data = getUserData(chat_id)  # Assuming getUserData function retrieves data for a user
    if user_data and 'data' in user_data:
        return user_data['data']  # Returns the list of transactions from user's data
    return []

#def show_spend_for_date(selected_date, chat_id, bot):
#    transactions = getUserHistory(chat_id)  # Assuming this retrieves all transactions for the user
#    
#    if transactions is None:  # Check if transactions are None
#        bot.send_message(chat_id, "No transactions found for the selected date.")
#        return
    
#    filtered_transactions = []

    # Filter transactions for the selected date
#    for txn in transactions:
#        txn_date_str = txn.split(',')[0].split(' ')[0]  # Ignore time if present
#        try:
            # Parse the transaction date string to a datetime object
#            txn_date = datetime.strptime(txn_date_str, '%d-%b-%Y')  # Assuming date is in '28-Sep-2024' format
#            if txn_date.date() == selected_date.date():  # Compare dates
#                filtered_transactions.append(txn)
#        except ValueError:
#            print(f"Unexpected transaction format: {txn}")

    # Send the filtered transactions back to the user
#    if filtered_transactions:
#        for txn in filtered_transactions:
#            bot.send_message(chat_id, f"{txn.split(',')[0]} - {txn.split(',')[1]}: ${txn.split(',')[2]}")
#    else:
#        bot.send_message(chat_id, "No transactions found for the selected date.")

def show_spend_for_date(selected_date, chat_id, bot):
    transactions = getTransactionsForChat(chat_id)  # Assuming this retrieves all transactions for the user
    filtered_transactions = []

    # Filter transactions for the selected date
    for txn in transactions:
        txn_date = datetime.strptime(txn.split(',')[0], '%d-%b-%Y')  # Assuming transactions have a 'date' field
        if txn_date.date() == selected_date.date():
            filtered_transactions.append(txn)

    # Send the filtered transactions back to the user
    if filtered_transactions:
        for txn in filtered_transactions:
            bot.send_message(chat_id, f"{txn.split(',')[0]} - {txn.split(',')[1]}: ${txn.split(',')[2]}")
    else:
        bot.send_message(chat_id, "No transactions found for the selected date.")


def display_remaining_overall_budget(message, bot):
    print('here')
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    print("here", remaining_budget)
    if remaining_budget >= 0:
        msg = '\nRemaining Overall Budget is $' + str(remaining_budget)
    else:
        msg = '\nBudget Exceded!\nExpenditure exceeds the budget by $' + \
            str(remaining_budget)[1:]
    bot.send_message(chat_id, msg)

def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(
        history) if str(query) in value]

    return float(budget) - calculate_total_spendings(queryResult)

def calculate_total_spendings(queryResult):
    total = 0

    for row in queryResult:
        s = row.split(',')
        total = total + float(s[2])
    return total

def display_remaining_category_budget(message, bot, cat):
    chat_id = message.chat.id
    remaining_budget = calculateRemainingCategoryBudget(chat_id, cat)
    if remaining_budget >= 0:
        msg = '\nRemaining Budget for ' + cat + ' is $' + str(remaining_budget)
    else:
        msg = '\nBudget for ' + cat + \
            ' Exceded!\nExpenditure exceeds the budget by $' + \
            str(abs(remaining_budget))
    bot.send_message(chat_id, msg)

def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(
        history) if str(query) in value]

    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)

def calculate_total_spendings_for_category(queryResult, cat):
    total = 0

    for row in queryResult:
        s = row.split(',')
        if cat == s[1]:
            total = total + float(s[2])
    return total

def getIncome(chat_id):
    data = getUserData(chat_id)
    if data is None or 'income' not in data:
        return None
    return data['income']

def setIncome(chat_id, income_value):
    user_list = read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = createNewUserRecord()
    user_list[str(chat_id)]['income'] = income_value
    write_json(user_list)

def getTotalSpendForMonth(chat_id):
    history = getUserHistory(chat_id)
    if history is None:
        return 0
    current_month = datetime.now().strftime('%b-%Y')
    monthly_spend = sum(float(txn.split(',')[2]) for txn in history if current_month in txn)
    return monthly_spend

def checkIfExceedsIncome(chat_id, amount_to_add, bot):
    income = getIncome(chat_id)
    if income is None:
        bot.send_message(chat_id, "You haven't set your monthly income. Please set your income using /income.")
        return True  # No income set, block the transaction until income is set

    total_spend = getTotalSpendForMonth(chat_id)
    
    # Check if the new expenditure exceeds the income
    if total_spend + amount_to_add > float(income):
        bot.send_message(chat_id, f"Transaction exceeds your monthly income limit! You have spent ${total_spend}, which exceeds your income of ${income}.")
        return True  # Exceeds income
    
    return False  # Income limit not exceeded, allow transaction


def getSpendCategories():
    with open("categories.txt", "r") as tf:
        spend_categories = tf.read().split(',')
    return spend_categories

def getplot():
    return plot

def getSpendDisplayOptions():
    return spend_display_option

def getSpendEstimateOptions():
    return spend_estimate_option

def getCommands():
    return commands

def getDateFormat():
    return dateFormat

def getTimeFormat():
    return timeFormat

def getMonthFormat():
    return monthFormat

def getChoices():
    return choices

def getBudgetOptions():
    return budget_options

def getBudgetTypes():
    return budget_types

def getUpdateOptions():
    return update_options

def getCategoryOptions():
    return category_options

