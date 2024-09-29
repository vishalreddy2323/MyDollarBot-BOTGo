import os
from unittest.mock import patch, ANY
from telebot import types
import sys

# Ensure helper is imported correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))
import category
import helper

def create_message(text):
    """Helper function to create a dummy message object"""
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

