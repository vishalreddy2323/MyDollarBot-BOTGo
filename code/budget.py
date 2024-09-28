import helper
import budget_view
import budget_update
import budget_delete
import budget_max
import logging
from telebot import types
from helper import convert_currency

def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getBudgetOptions()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Operation', reply_markup=markup)
    bot.register_next_step_handler(msg, post_operation_selection, bot)
# budget.py

def get_total_expenses_in_base_currency(expenses, base_currency):
    total = 0
    for expense in expenses:
        amount = expense['amount']
        currency = expense['currency']
        converted_amount = convert_currency(amount, currency, base_currency)
        total += converted_amount
    return total

def check_budget_limit(expenses, budget_limit, base_currency):
    total_spent = get_total_expenses_in_base_currency(expenses, base_currency)
    if total_spent > budget_limit:
        return f"Warning! You have exceeded your budget of {budget_limit} {base_currency}. You have spent {total_spent}."
    return f"You are within your budget. Total spent: {total_spent} {base_currency}."


def post_operation_selection(message, bot):
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getBudgetOptions()
        if op not in options.values():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry, I don't recognise this operation \"{}\"!".format(op))
        if op == options['update']:
            budget_update.run(message, bot)
        elif op == options['view']:
            budget_view.run(message, bot)
        elif op == options['delete']:
            budget_delete.run(message, bot)
        elif op == options['max_spend']:
            budget_max.run(message, bot)

    except Exception as e:
        helper.throw_exception(e, message, bot, logging)
