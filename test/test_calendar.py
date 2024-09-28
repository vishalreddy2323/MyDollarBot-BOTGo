import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
import helper


# Mock the getTransactionsForChat function to return sample transactions
@pytest.fixture
def mock_transactions():
    return [
        '28-Sep-2024,Food,50.0',
        '28-Sep-2024,Groceries,20.0',
        '29-Sep-2024,Utilities,100.0'
    ]


# Test function for show_spend_for_date
def test_show_spend_for_date(mocker, mock_transactions):
    chat_id = 12345
    selected_date = datetime.strptime('2024-09-28', '%Y-%m-%d')

    # Patch getTransactionsForChat to return mock transactions
    mocker.patch.object(helper, 'getTransactionsForChat', return_value=mock_transactions)

    # Mock the bot's send_message function
    mock_bot = MagicMock()

    # Call the function with the mocked data
    helper.show_spend_for_date(selected_date, chat_id, mock_bot)

    # Check if the correct messages were sent for the selected date
    expected_calls = [
        mocker.call(chat_id, '28-Sep-2024 - Food: $50.0'),
        mocker.call(chat_id, '28-Sep-2024 - Groceries: $20.0')
    ]

    # Assert that the bot sent the expected messages
    mock_bot.send_message.assert_has_calls(expected_calls)


# Test function for no transactions found
def test_show_spend_for_date_no_transactions(mocker):
    chat_id = 12345
    selected_date = datetime.strptime('2024-10-01', '%Y-%m-%d')

    # Patch getTransactionsForChat to return empty or non-matching transactions
    mocker.patch.object(helper, 'getTransactionsForChat', return_value=[
        '28-Sep-2024,Food,50.0',
        '28-Sep-2024,Groceries,20.0',
        '29-Sep-2024,Utilities,100.0'
    ])

    # Mock the bot's send_message function
    mock_bot = MagicMock()

    # Call the function with the mocked data
    helper.show_spend_for_date(selected_date, chat_id, mock_bot)

    # Assert that the bot sent the "No transactions found" message
    mock_bot.send_message.assert_called_once_with(chat_id, "No transactions found for the selected date.")

