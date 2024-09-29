from code import helper
from code.helper import validate_transaction_limit
from telebot import types
from unittest.mock import patch, MagicMock, ANY

MOCK_CHAT_ID = 101
MOCK_USER_DATA = {
    str(MOCK_CHAT_ID): {
        'data': ["correct_mock_value"],
        'budget': {
            'overall': None,
            'category': None
        }
    },
    '102': {
        'data': ["wrong_mock_value"],
        'budget': {
            'overall': None,
            'category': None
        }
    }
}

# Helper function to create a message
def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_throw_exception(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("message from testing")
    helper.throw_exception(Exception("Test exception"), message, mc, MagicMock())
    assert mc.send_message.called

def test_getUserHistory_with_data(mocker):
    # Simulate valid user data
    mocker.patch.object(helper, 'read_json')
    helper.read_json.return_value = MOCK_USER_DATA
    result = helper.getUserHistory(MOCK_CHAT_ID)
    assert result == MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data'], 'User data is available but not found'


@patch('telebot.telebot')
def test_validate_transaction_limit_within_limit(mock_telebot, mocker):
    # Test when the transaction limit is within bounds
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    validate_transaction_limit(MOCK_CHAT_ID, 50.0, mc)
    mc.reply_to.assert_not_called()


# Validation tests for entered amounts
def test_validate_entered_amount_none():
    result = helper.validate_entered_amount(None)
    assert not result, 'None is not a valid amount'

def test_validate_entered_amount_int():
    val = '101'
    result = helper.validate_entered_amount(val)
    assert result, f'{val} is a valid amount'

def test_validate_entered_amount_int_max():
    val = '999999999999999'
    result = helper.validate_entered_amount(val)
    assert result, f'{val} is a valid amount'

def test_validate_entered_amount_int_outofbound():
    val = '9999999999999999'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is out of bound'

def test_validate_entered_amount_float():
    val = '101.11'
    result = helper.validate_entered_amount(val)
    assert result, f'{val} is a valid amount'

def test_validate_entered_amount_float_max():
    val = '999999999999999.9999'
    result = helper.validate_entered_amount(val)
    assert result, f'{val} is a valid amount'

def test_validate_entered_amount_float_more_decimal():
    val = '9999999999.999999999'
    result = helper.validate_entered_amount(val)
    assert result, f'{val} is a valid amount'

def test_validate_entered_amount_float_outofbound():
    val = '9999999999999999.99'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is out of bound'

def test_validate_entered_amount_string():
    val = 'invalidamount'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is not a valid amount'

def test_validate_entered_amount_string_with_dot():
    val = 'invalid.amt'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is not a valid amount'

def test_validate_entered_amount_special_char():
    val = '$%@*@.@*'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is not a valid amount'

def test_validate_entered_amount_alpha_num():
    val = '22e62a'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is not a valid amount'

def test_validate_entered_amount_mixed():
    val = 'a14&^%.hs827'
    result = helper.validate_entered_amount(val)
    assert not result, f'{val} is not a valid amount'


def test_getSpendCategories():
    result = helper.getSpendCategories()
    assert result == helper.spend_categories, 'expected spend categories are not returned'

def test_getSpendDisplayOptions():
    result = helper.getSpendDisplayOptions()
    assert result == helper.spend_display_option, 'expected spend display options are not returned'

def test_getCommands():
    result = helper.getCommands()
    assert result == helper.commands, 'expected commands are not returned'

def test_getDateFormat():
    result = helper.getDateFormat()
    assert result == helper.dateFormat, 'expected date format is not returned'

def test_getTimeFormat():
    result = helper.getTimeFormat()
    assert result == helper.timeFormat, 'expected time format is not returned'

def test_getMonthFormat():
    result = helper.getMonthFormat()
    assert result == helper.monthFormat, 'expected month format is not returned'

def test_getChoices():
    result = helper.getChoices()
    assert result == helper.choices, 'expected choices are not returned'

def test_write_json(mocker):
    mocker.patch.object(helper, 'json')
    helper.json.dump.return_value = True
    user_list = ['hello']
    helper.write_json(user_list)
    helper.json.dump.assert_called_with(user_list, ANY, ensure_ascii=ANY, indent=ANY)

def test_createNewUserRecord():
    data_format_call = helper.createNewUserRecord()
    data_format = {
        'data': [],
        'budget': {
            'overall': None,
            'category': None
        }
    }
    assert sorted(data_format_call) == sorted(data_format)

