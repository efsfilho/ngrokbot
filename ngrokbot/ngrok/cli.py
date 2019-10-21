from .util import *
from .ngrok import NgrokManager


def cli():
    print('CLI Started')
    ngrok = NgrokManager()
    ngrok.get_ngrok()

    while True:
        cmd = input()
        cmd = split_text(cmd)
        if cmd[0] == 'exit':
            ngrok.stop()
            break

        if cmd[0] == 'start':
            if len(cmd) > 1:
                args = []
                for arg in cmd:
                    if arg != 'start':
                        args.append(arg)
                print(args)
                ngrok.start(args)
            else:
                ngrok.start()

        if cmd[0] == 'getinfo': print(ngrok.get_info())
        if cmd[0] == 'getfullinfo': print(ngrok.get_info(True))
        if cmd[0] == 'stdout': print(ngrok.get_stdout())
        if cmd[0] == 'stop': ngrok.stop()
    
    print('CLI Finished')