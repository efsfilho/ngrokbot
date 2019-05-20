#!/usr/bin/python3

import os
import sys
import pathlib
import zipfile
import platform
import tempfile
import urllib.request
from urllib.error import URLError, HTTPError

def get_platform():
    os = {}
    os['os'] = platform.system()

    if platform.machine() in {'x86_64', 'AMD64'}:
        os['arch'] = 64
    else:
        os['arch'] = 32

    print('Platform:', os['os'], os['arch'])

    if os['os'] != 'Linux' and os['os'] != 'Windows':
        raise ValueError('Platform not supported')
    return os

def download_file(url, filename):
    try:
        print('Downloading ngrok...', url)
        urllib.request.urlretrieve(url, filename)
    except HTTPError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e)
    except URLError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e.reason)
    
def get_ngrok():
    try:
        plat = get_platform()
        if plat['os'] == 'Windows':
            filename = 'ngrok.exe'
            if plat['arch'] == 64:
                url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip'
            else:
                url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-386.zip'
        else:
            filename = 'ngrok'
            if plat['arch'] == 64:
                url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
            else:
                url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'

        temp = tempfile.gettempdir()
        ngrok_zip_path = pathlib.Path(temp, 'ngrok.zip')
        ngrok_exe_path = pathlib.Path(temp, filename)

        download_file(url, ngrok_zip_path)

        zip_file = zipfile.ZipFile(ngrok_zip_path, 'r')
        zip_file.extractall(temp)
        zip_file.close()
        os.chmod(ngrok_exe_path, 0o755)

    except ValueError as err:
        print(err)
        sys.exit(1)

get_ngrok()