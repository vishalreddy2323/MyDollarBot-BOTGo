# Max Transaction Limit Management in Telegram Bot

This document provides an overview of the Python script used in a Telegram bot for managing the maximum transaction limit. Users can set their maximum transaction limit using this script.

## Functions and Methods

### run(message, bot)
This function initiates the process of managing the maximum transaction limit.

- `message`: The message object received from the user in the chat.
- `bot`: The bot instance used to interact with the Telegram API.

### post_max_budget(message, bot)
This function handles the user's input for setting the new maximum transaction limit and updates the user's records.

- `message`: The message object received from the user with the new maximum transaction limit.
- `bot`: The bot instance used to interact with the Telegram API.

### Dependencies
- The script relies on the `helper` module for various functions such as checking the current maximum limit, validating user input, and updating user records.
- It uses the `telebot` module for interacting with the Telegram bot.