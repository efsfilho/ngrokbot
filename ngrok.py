#!/usr/bin/python3

import os
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

def report_hook(blocknum, blocksize, totalsize):
    read = blocknum * blocksize
    if totalsize > 0:
        percent = read * 1e2 / totalsize
        readf = read/math.pow(1024, 2)
        totalf = totalsize/math.pow(1024, 2)
        sys.stderr.write(f"\r {percent:.0f}% {readf:.2f}Mb of {totalf:.2f}Mb")
        if read >= totalsize:
            # end
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (read,))
            
def download_file(url, filename):
    try:
        print('Downloading ngrok... ', url)
        urllib.request.urlretrieve(url, filename, report_hook)
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

        download = ngrok_exe_path.is_file()

        if not download:
            download_file(url, ngrok_zip_path)
            print('Extracting ngrok: ', ngrok_zip_path)
            zip_file = zipfile.ZipFile(ngrok_zip_path, 'r')
            zip_file.extractall(temp)
            zip_file.close()
            os.chmod(ngrok_exe_path, 0o755)

        return ngrok_exe_path
    except ValueError as err:
        print(err)
        sys.exit(1)

ngrok_process = None
def execute():
    global ngrok_process
    filePath = get_ngrok()
    filePathStr = str(filePath)
    try:
        token = '--authtoken=asd'
        # p = subprocess.run([filePathStr, 'http', '80'], capture_output=False)
        ngrok_process = subprocess.Popen([filePathStr, 'http', '80'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout, stderr = p.communicate()
    except Exception as err:
        print(err)

def getInfo(full=False):
    try:
        res = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels').read()
        api = json.loads(res.decode('utf-8'))
        if full:
            return api['tunnels'][0]
        else:
            return api['tunnels'][0]['public_url']
    except HTTPError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e)
    except URLError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e.reason)



execute()

info = getInfo()
print(info)

time.sleep(5.0)
ngrok_process.kill()
print('end')
