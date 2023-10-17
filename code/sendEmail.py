import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import ssl
from email import encoders
import os.path
from telebot import types
import threading
import helper
import csv

extract_complete = threading.Event()
# Function to send an email
def send_email(user_email, subject, message, attachment_path):
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "dollarbot123@gmail.com"
    email_to = user_email
    pswd = "tsvueizeuvzivtjo"   # App password 

    # Make the body of the email
    body = message

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Define the file to attach
    filename = attachment_path

    # Open the file in python as a binary
    attachment = open(filename, 'rb')  # r for read and b for binary

    # Encode as base 64
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)

    # Cast as string
    text = msg.as_string()

        # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()

    # Send emails to "person" as list is iterated
    print(f"Sending email to: {email_to}...")
    TIE_server.sendmail(email_from, email_to, text)
    print(f"Email sent to: {email_to}")
    print()

    # Close the port
    TIE_server.quit()

# Function to run the main process
def run(message, bot):
    try:
        chat_id = message.chat.id
        # with open('code/data.csv', 'rb') as file:
        #     bot.send_document(chat_id, document=file) 
        bot.send_message(chat_id, 'Extracting data')
        user_history = helper.getUserHistory(chat_id)
        if not user_history:
            bot.send_message(chat_id, "no data to generate csv, hence email not being sent")
        else:   
            file_path = 'code/data.csv'
            rows = [line.split(',') for line in user_history]
            column_names = ['Date and Time', 'Category', 'Amount']
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)
            # Send the file to the user
            message = bot.send_message(chat_id, 'Please enter your email: ')
            bot.register_next_step_handler(message, process_email_input)     
            #os.remove(file_path)    
    except Exception as e:
        logging.error(str(e))    


# Function for sending all parameters to email
def process_email_input(message):
    user_email = message.text

    # Compose the email
    email_subject = "DollarBot Budget Report"
    email_message = f"Hello {user_email},\n\nPFA the budget report that you requested."

    check_file = os.path.isfile('code/data.csv')
    # Send the email
    if check_file:
        send_email(user_email, email_subject, email_message, 'code/data.csv')
        os.remove('code/data.csv')