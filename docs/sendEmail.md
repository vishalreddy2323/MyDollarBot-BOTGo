# DollarBot Email Sender

This document provides an overview of the Python script for sending budget reports via email using the "DollarBot" application. This script uses the Gmail SMTP server to send emails with budget reports as attachments.

## Functions and Methods

### send_email(user_email, subject, message, attachment_path)
This function sends an email to the specified user.

- `user_email`: The recipient's email address.
- `subject`: The subject of the email.
- `message`: The main body of the email.
- `attachment_path`: The path to the file to be attached to the email.

### run(message, bot)
This function initiates the main process. It prompts the user to enter their email address.

- `message`: The message object.
- `bot`: A reference to the chatbot.

### process_email_input(message, bot)
This function processes the user's email input and sends the budget report.

- `message`: The message object containing the user's email input.
- `bot`: A reference to the chatbot.
