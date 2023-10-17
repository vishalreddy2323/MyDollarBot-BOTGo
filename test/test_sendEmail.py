import unittest
from unittest.mock import patch, Mock
from code.sendEmail import send_email
import os

#this test checks the configuration of the smtp server
@patch('code.sendEmail.smtplib.SMTP')
def test_send_email(mock_smtp):
    # Set up your mock SMTP server
    mock_server = Mock()
    mock_smtp.return_value = mock_server

    user_email = "example@example.com"
    subject = "Test Subject"
    message = "Test Message"
    attachment_path = 'test_attachment.txt'  # Use the file name

    # Create a dummy test attachment file
    with open('test_attachment.txt', 'w') as dummy_file:
        dummy_file.write("This is a test attachment.")

    try:
        send_email(user_email, subject, message, attachment_path)

        # Check that the SMTP server is called with the correct arguments
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("dollarbot123@gmail.com", "tsvueizeuvzivtjo")
        mock_server.sendmail.assert_called_once_with("dollarbot123@gmail.com", user_email, mock_server.sendmail.call_args[0][2])
        mock_server.quit.assert_called_once()

    finally:
        # Remove the dummy test attachment file
        os.remove('test_attachment.txt')

if __name__ == '__main__':
    unittest.main()