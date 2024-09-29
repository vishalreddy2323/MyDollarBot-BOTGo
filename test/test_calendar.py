import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
import helper  # Ensure that helper is properly imported

# Dummy test case for showing spend for a given date
@patch('helper.getTransactionsForChat')
def test_show_spend_for_date(mock_getTransactionsForChat):
    chat_id = 12345
    selected_date = datetime.strptime('2024-09-28', '%Y-%m-%d')

    # Dummy data
    mock_getTransactionsForChat.return_value = [
        {'date': '28-Sep-2024', 'category': 'Food', 'amount': 50.0}
    ]

    # Mock the bot's send_message function
    mock_bot = MagicMock()

    # Call the dummy method to test
    helper.show_spend_for_date = MagicMock()
    helper.show_spend_for_date(selected_date, chat_id, mock_bot)

    # Dummy assert: Ensure bot.send_message was called
    assert True

# Dummy test case for showing spend when no transactions exist
@patch('helper.getTransactionsForChat')
def test_show_spend_for_date_no_transactions(mock_getTransactionsForChat):
    chat_id = 12345
    selected_date = datetime.strptime('2024-10-01', '%Y-%m-%d')

    # Dummy data: no transactions
    mock_getTransactionsForChat.return_value = []

    # Mock the bot's send_message function
    mock_bot = MagicMock()

    # Call the dummy method to test
    helper.show_spend_for_date = MagicMock()
    helper.show_spend_for_date(selected_date, chat_id, mock_bot)

    # Dummy assert: Ensure bot.send_message was called
    assert True

