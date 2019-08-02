#!/usr/bin/python3

import os
import re
import sys
import json
import math
import time
import pathlib
import zipfile
import tempfile
import platform
import subprocess
import urllib.request
from urllib.error import URLError, HTTPError

# stderr, stdout and pid of the running ngrok
ngrok_process = None

def get_platform():
    """
    Returns OS/Architecture
    """
    os = dict(os='', arch='')
    os['os'] = platform.system()

    if platform.machine() in {'x86_64', 'AMD64'}:
        os['arch'] = 64
    else:
        os['arch'] = 32

    print('Platform:', os['os'], os['arch'])

    if os['os'] != 'Linux' and os['os'] != 'Windows':
        raise ValueError('Platform not supported yet!')
    return os

def get_ngrok_url():
    """
    Returns ngrok url to be download according to the running platform
    """
    url = ''
    plat = get_platform()
    if plat['os'] == 'Linux':
        if plat['arch'] == 64:
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
        else:
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'
    else:
        if plat['arch'] == 64:
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip'
        else:
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-386.zip'
        
    return url

def report_hook(block_num, block_size, total_size):
    """
    Write download progress
    """
    read = block_num * block_size
    if total_size > 0:
        percent = read * 1e2 / total_size
        readf = read/math.pow(1024, 2)
        totalf = total_size/math.pow(1024, 2)
        sys.stderr.write(f"\r {percent:.0f}% {readf:.2f}Mb of {totalf:.2f}Mb")
        if read >= total_size:
            # end
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (read,))

def download_file(file_name):
    try:
        url = get_ngrok_url()
        print('Downloading ngrok... ', url)
        urllib.request.urlretrieve(url, file_name, report_hook)
    except HTTPError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e)
    except URLError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e.reason)

def get_ngrok():
    """
    Returns ngrok executable path after download and extract ngrok to the temp directory
    """

    if get_platform()['os'] == 'Linux':
        file_name = 'ngrok'
    else:
        file_name = 'ngrok.exe'

    temp = tempfile.gettempdir()
    ngrok_path = pathlib.Path(temp, file_name)

    try:
        # checks if ngrok was already downloaded
        if ngrok_path.is_file():
            return ngrok_path
        else:
            temp = tempfile.gettempdir()
            ngrok_zip_path = pathlib.Path(temp, 'ngrok.zip')

            # downloads ngrok zip
            download_file(ngrok_zip_path)

            print('Extracting ngrok: ',ngrok_zip_path)

            zip_file = zipfile.ZipFile(ngrok_zip_path, 'r')
            zip_file.extractall(temp)
            zip_file.close()

            os.chmod(ngrok_path, 0o755)

            if ngrok_path.is_file():
                return ngrok_path
            else:
                # TODO else 
                raise ValueError('It was not possible to get ngrok executable.')

    except ValueError as err:
        print(err)
        sys.exit(1)

def get_stdout():
    global ngrok_process
    msg = ''
    if not is_running():
        for line in ngrok_process.stdout:
            msg += line.decode('utf-8')
            # print('', line.decode('utf-8'))
    return msg

def is_running():
    """
    Returns True if ngrok process is running
    """
    global ngrok_process
    if ngrok_process is None:
        return False
    else:
        if ngrok_process.poll() is None:
            return True
        else:
            return False

def execute(args_text=''):
    global ngrok_process

    if is_running():
        print('ngrok already running')
        return

    filePath = get_ngrok()
    filePathStr = str(filePath)
    try:
        token = '--authtoken=asd'

        if args_text == '':
            args = ['http', '3000']
        else:
            args = split_text(args_text)       

        args.insert(0, filePathStr)

        ngrok_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('ngrok Running...', args)
        # stdout, stderr = ngrok_process.communicate()
    except ValueError as err:
        print(err)

def stop():
    global ngrok_process
    if ngrok_process != None:
        ngrok_process.terminate()
        ngrok_process = None
        print('ngrok stoped.')

def get_info(full=False):
    try:
        local_api = 'http://127.0.0.1:4040/api/tunnels'
        res = urllib.request.urlopen(local_api).read()
        api = json.loads(res.decode('utf-8'))
        if full:
            return api['tunnels'][0]
        else:
            return api['tunnels'][0]['public_url']
    except HTTPError as e:
        raise ValueError('An error has occurred while accessing ngrok local api: '+local_api, e)
    except URLError as e:
        raise ValueError('An error has occurred while accessing ngrok local api: '+local_api, e.reason)

def split_text(text):
    if not isinstance(text, str):
        raise TypeError('text is not a str.')

    replaced_text = re.sub(r'[^0-9a-zA-Z\s]', '', text)
    return replaced_text.split()

# while True:
#     cmd = input()
#     cmd = split_text(cmd)
#     args = []
#     if len(cmd) < 1: break
#     if cmd[0] == 'exit': 
#         stop() 
#         break
#     if cmd[0] == 'stop': stop()
#     if cmd[0] == 'start': execute('-h')
#     if cmd[0] == 'getinfo': print(get_info())
#     if cmd[0] == 'getfullinfo': print(get_info(True))
#     if cmd[0] == 'isrunning': print(is_running())
#     if cmd[0] == 'stdout': print(get_stdout())
#     if cmd[0] == 'split': print(split_text('aaa sdd@#$@#$ $#/ ¨¨&*7*( 23cvfcv'))
    