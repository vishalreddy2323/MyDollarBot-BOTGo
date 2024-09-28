from unittest.mock import MagicMock
import pytest
from code import income  # Ensure this import points to where your income processing code is located

@pytest.mark.parametrize("income_value, expected_message", [
    (1000.0, "Your monthly income has been set to $1000."),
    (500.0, "Your monthly income has been set to $500."),
    (0.0, "Your monthly income has been set to $0.")
])
def test_income_input(mocker, income_value, expected_message):
    chat_id = 12345

    # Mock the helper functions to read and write JSON
    mocker.patch('helper.read_json', return_value={})
    mocker.patch('helper.write_json')

    # Mock the bot's send_message function
    mock_bot = MagicMock()

    # Simulate a message from the user
    message = MagicMock()
    message.chat.id = chat_id
    message.text = str(income_value)

    # Call the process_income_input to simulate the income setting process
    income.process_income_input(message, mock_bot)

    # Normalize the actual message by removing trailing zeros and decimal places if not necessary
    actual_message = mock_bot.send_message.call_args[0][1]
    actual_message = actual_message.replace(".0", "")  # Remove the trailing .0 for comparison

    # Normalize the expected message similarly
    expected_message_with_decimal = expected_message.replace(".", ".0")

    # Compare the normalized actual message with both expected formats
    assert actual_message in {expected_message, expected_message_with_decimal}, \
        f"Expected: {expected_message} or {expected_message_with_decimal}, but got: {actual_message}"

