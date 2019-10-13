#!/usr/bin/python3

import re
import sys
import math
import platform
import urllib.request
from urllib.error import  URLError, HTTPError

def get_platform():
    """ Returns OS/Architecture """
    os = dict(os='', arch='')
    os['os'] = platform.system()

    if platform.machine() in {'x86_64', 'AMD64'}:
        os['arch'] = 64
    else:
        os['arch'] = 32

    if os['os'] != 'Linux' and os['os'] != 'Windows':
        raise ValueError('Platform not supported yet!')
    return os

def get_ngrok_url():
    """ Returns ngrok url to be download according to the running platform """
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
    """ Write download progress """
    read = block_num * block_size
    if total_size > 0:
        percent = read * 1e2 / total_size
        readf = read/math.pow(1024, 2)
        totalf = total_size/math.pow(1024, 2)

        sys.stderr.write(f'\rDownloading..........: {percent:.0f}% {readf:.2f}Mb of {totalf:.2f}Mb')

        if read >= total_size:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (read,))

def download_file(file_name):
    try:
        url = get_ngrok_url()
        print(f'Ngrok source.........: {url}')
        urllib.request.urlretrieve(url, file_name, report_hook)
    except HTTPError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e)
    except URLError as e:
        raise ValueError('An error has occurred while downloading ngrok:', e.reason)

def split_text(text):
    if not isinstance(text, str):
        raise TypeError('text is not a str.')

    replaced_text = re.sub(r'[^0-9a-zA-Z\s]', '', text)
    return replaced_text.split()