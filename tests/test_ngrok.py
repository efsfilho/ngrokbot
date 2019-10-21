import pytest
import time
from ngrokbot import NgrokManager


ngrok = NgrokManager()

def test_get_stdout():
    assert ngrok.get_stdout() == ''

def test_get_ngrok():
    assert ngrok.get_ngrok()

