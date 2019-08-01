import pytest
import time

from src.ngrok import app

def check_keys(dictObj, key):
    __tracebackhide__ = True

    if isinstance(dictObj, dict):
        if not key in dictObj.keys():
            pytest.fail('%s key not found.' % (key,))
    else:
        raise TypeError('Object is not a dict type.')

def test_get_platform():
    info = app.get_platform()
    check_keys(info, 'os')
    check_keys(info, 'arch')

    assert info['os'] == 'Linux' or info['os'] == 'Windows'

def test_execute():
    app.execute()
    assert app.is_running() == True
    assert type(app.get_info()) == str
    app.stop()

# while True:
#     cmd = input()
#     if cmd == 'exit': 
#         stop() 
#         break
#     if cmd == 'e': stop()
#     if cmd == 'start': execute()
#     if cmd == 'i': print(get_info())
#     if cmd == 'if': print(get_info(True))
#     if cmd == 'c': print(is_running())
#     if cmd == 's': print(get_stdout())