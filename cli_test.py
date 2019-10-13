#!/usr/bin/python3
import re

def split_text(text):
    if not isinstance(text, str):
        raise TypeError('text is not a str.')

    replaced_text = re.sub(r'[^0-9a-zA-Z\s]', '', text)
    return replaced_text.split()

from ngrok import *

n = NgrokManager()
n.get_ngrok()

while True:
    cmd = input()
    cmd = split_text(cmd)
    if cmd[0] == 'exit':
        n.stop()
        break

    if cmd[0] == 'start':
        if len(cmd) > 1:
            args = []
            for arg in cmd:
                if arg != 'start':
                    args.append(arg)
            print(args)
            n.start(args)
        else:
            n.start()

    if cmd[0] == 'getinfo': print(n.get_info())
    if cmd[0] == 'getfullinfo': print(n.get_info(True))
    if cmd[0] == 'stdout': print(n.get_stdout())

    if cmd[0] == 'stop':
        n.stop()


        
print('Finish')