from unittest.mock import ANY
from unittest.mock import patch
from types import SimpleNamespace  # Correct import
from telebot import types
from code import add
import pytest

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'



def create_message(text):
    message = SimpleNamespace()  # Creating a mock message object
    message.text = text
    message.chat = SimpleNamespace(id=12345)  # Simulating the chat ID
    return message


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Test message")

    add.run(message, mc)

    assert mc.reply_to.called
    assert "Test message" in message.text


@patch('telebot.telebot')
def test_post_category_selection_working(mocker):
    mocker.patch('helper.get_help_text', return_value="Here is some help text")
    mock_telebot = mocker.patch('telebot.telebot')
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from testing!")
    add.post_category_selection(message, mc)



@patch('telebot.telebot')
def test_post_category_selection_noMatchingCategory(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True

    mocker.patch.object(add, 'helper')
    add.helper.getCategories.return_value = []

    message = create_message("Invalid category test")
    add.post_category_selection(message, mc)

    assert mc.reply_to.called
    assert 'Oh no! Sorry I don\'t recognize this category "Invalid category test"!' in mc.reply_to.call_args[0][1]


@patch('telebot.telebot')
def test_post_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 10  # Mock a valid non-zero amount
    add.helper.getDateFormat.return_value = '%d-%b-%Y'  # Mock the correct date format string
    add.helper.getTimeFormat.return_value = '%H:%M'     # Mock the correct time format string

    # Ensure the chat ID exists in the option dictionary
    mocker.patch.object(add, 'option', {12345: "Food"})  # Mock add.option to contain the chat ID

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food")  # Pass a valid category as the selected_category

    assert mc.send_message.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat

    mocker.patch.object(add, 'option')
    add.option = {12345: "here"}  # Ensure the chat ID exists in the option dictionary

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Groceries")  # Pass a valid category

    assert mc.send_message.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 0

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Transport")  # Pass a valid category

    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat

    mocker.patch.object(add, 'option')
    add.option = {12345: "here"}  # Ensure the chat ID exists in the option dictionary

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Miscellaneous")  # Pass a valid category

    assert mc.send_message.called
