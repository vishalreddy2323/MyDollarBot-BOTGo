# About MyDollarBot's /receipt Feature
This feature enables the user to retrieve receipts in an image format of their expenses for a particular date.
Currently we have the following expense categories set by default:

# File: receipt_bot.py

This Markdown document provides a concise overview of the Python script named `receipt_bot.py`. This script is responsible for implementing a Telegram bot that allows users to retrieve receipts based on a specified date.

## Overview
The script uses several Python libraries and the Telegram Bot API to interact with users. It reads configuration data from a `user.properties` file, including the Telegram API token required for the bot to function.

## Dependencies
The script relies on the following Python libraries:
- `logging`: Used for error logging.
- `telebot`: Provides functionalities to interact with the Telegram Bot API.
- `jproperties`: Used for reading configuration data from `user.properties`.
- `datetime`: Required for date format validation.
- `glob`: Used for searching and retrieving receipts.

## Key Components
### Loading Configuration
- The script reads the Telegram API token from the `user.properties` file.

### `command_receipt(message, bot)`
- Method for handling the `/receipt` command.
- Accepts a `message` object and a `bot` instance as parameters.
- Requests the user to input a date in the format `YYYY-MM-DD` or `YYYYMMDD`.
- Registers the next step handler for processing the date input.

### `process_date_input(message)`
- Method for processing user input for the date.
- Validates the date format and handles any errors.
- Searches for receipt files with filenames containing the specified date.
- Sends matching receipts as photos to the user.
- Handles exceptions and logs errors using the `logging` module.

## Usage
To use this script, you need to create a `user.properties` file with your Telegram API token. Users can interact with the bot by sending the `/receipt` command and providing a valid date in the requested format.

Please note that this Markdown document provides a detailed description of the methods used in the script. For the complete code and detailed implementation, refer to the `receipt_bot.py` file.
