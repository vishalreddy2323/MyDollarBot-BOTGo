import helper
import logging
from telebot import types
import csv
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email, smtplib, ssl

from email import encoders
# Function to send an email
def send_email(user_email, subject, message, attachment_path):
    print("trying to sernd emsil")
    # Email configuration
    sender_email = "dollarbot123@gmail.com"
    password = "tsvueizeuvzivtjo"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, "plain"))

    # Attach the CSV file
    with open(attachment_path, 'rb') as file:
        part = MIMEBase("application", "octet-stream")
        # attachment = MIMEText(file.read())
        part.set_payload(file.read())

    encoders.encode_base64(part)

    part.add_header(
    "Content-Disposition",
    f"file; filename= {attachment_path}",
    )

    msg.attach(part)
    text = msg.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 587, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, user_email, text)  

def sendemail1(user_email, subject, message, attachment_path):
    smtp_port = 465                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    # Set up the email lists
    email_from = "dollarbot123@gmail.com"
    email_list = user_email

    # Define the password (better to reference externally)
    pswd = "tsvueizeuvzivtjo" # As shown in the video this password is now dead, left in as example only

    # Make the body of the email
    body = message

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_list
    msg['Subject'] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Define the file to attach
    filename = attachment_path

    # Open the file in python as a binary
    attachment= open(filename, 'rb')  # r for read and b for binary

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
    print(f"Sending email to: {email_list}...")
    TIE_server.sendmail(email_from, email_list, text)
    print(f"Email sent to: {email_list}")
    print()

    # Close the port
    TIE_server.quit()

# Function to run the main process
def run(message, bot):

    try:
        chat_id = message.chat.id
        with open('code/data.csv', 'rb') as file:
            bot.send_document(chat_id, document=file) 

        message = bot.send_message(chat_id, 'Please enter your email')
        bot.register_next_step_handler(message, process_email_input)        

    except Exception as e:
        logging.error(str(e))

    # print("All emails sent and Telegram notifications sent.")

def process_email_input(message):
    user_email = message.text

    # Compose the email
    email_subject = "DollarBot Budget Report"
    email_message = f"Hello ,\n\nPFA the budget report that you requested."

    # Send the email
    send_email(user_email, email_subject, email_message, 'code/data.csv')

