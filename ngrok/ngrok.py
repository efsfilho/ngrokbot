#!/usr/bin/python3

import os
import json
import pathlib
import zipfile
import tempfile
import subprocess
from .util import *

class NgrokManager():

    def __init__(self):
        self.__ngrok_instalation_path = None
        self.__ngrok_executable = None
        self.__ngrok_process = None

    def __install_ngrok(self, path=None, force=False):
        """ 
        Download and extract ngrok

        Parameters
        ----------
        path : str
            Installation path
        force:
            True to download and replace ngrok executable if it is already installed
        
        Returns
        -------
        ngrok_path : str or None
            ngrok executable path or None if something went wrong

        """
        platform = get_platform()
        if platform['os'] == 'Linux':
            file_name = 'ngrok'
        else:
            file_name = 'ngrok.exe'
        print('Platform.............:',platform['os'], platform['arch'])

        try:
            if path is None:
                temp = pathlib.Path(tempfile.gettempdir(),'ngrok')

                if not os.path.exists(temp) and not os.path.isdir(temp):
                    os.mkdir(temp)

                ngrok_instalation_path = temp
            else:
                if os.path.isdir(path) and os.path.exists(path):
                    ngrok_instalation_path = path
                else:
                    raise Exception('Path informed does not exist or is not a directory.')

            ngrok_path = pathlib.Path(ngrok_instalation_path, file_name)

            # checks if ngrok was already downloaded
            if ngrok_path.is_file() and not force:
                return ngrok_path
            else:

                ngrok_zip_path = pathlib.Path(ngrok_instalation_path, 'ngrok.zip')

                # downloads ngrok zip
                download_file(ngrok_zip_path)

                print(f'Extracting ngrok from: {ngrok_zip_path}')

                zip_file = zipfile.ZipFile(ngrok_zip_path, 'r')
                zip_file.extractall(ngrok_instalation_path)
                zip_file.close()

                os.chmod(ngrok_path, 0o755)

                if ngrok_path.is_file():
                    return ngrok_path
                else:
                    return None

        except ValueError as error:
            print('Error: ', error)

    def __is_ngrok_running(self):
        """
        Returns True if ngrok process is running
        """
        if self.__ngrok_process is None:
            return False
        else:
            if self.__ngrok_process.poll() is None:
                return True
            else:
                return False

    def get_ngrok(self):
        print('NgrokManager starting...')
        self.__ngrok_executable = self.__install_ngrok()

        if self.__ngrok_executable != None:
            print(f'Ngrok executable.....: {self.__ngrok_executable}\n')

    def start(self, args_list=None):
        if self.__is_ngrok_running():
            print('ngrok is already running!')
            return

        if self.__ngrok_executable == None:
            self.__ngrok_executable = self.__install_ngrok()
            if self.__ngrok_executable == None:
                # TODO download erros handling
                return

        try:
            token = '--authtoken=asd'

            if args_list == None:
                args = ['http', '3000']
            else:
                args = args_list
            args.insert(0, self.__ngrok_executable)

            self.__ngrok_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            args.remove(args[0])
            args_str = ' '.join(args)
            print(f'running {self.__ngrok_executable} {args_str}')
            print(f'PID {self.__ngrok_process.pid} ')

        except Exception as error:
            print('Error: ', error)

    def stop(self):
        if self.__is_ngrok_running():
            self.__ngrok_process.terminate()
            self.__ngrok_process = None
        print('ngrok stoped')

    def get_stdout(self):
        msg = ''
        if not self.__is_ngrok_running():
            for line in self.__ngrok_process.stdout:
                msg += line.decode('utf-8')
        return msg

    def get_info(self, full=False):
        try:
            if self.__is_ngrok_running():
                local_api = 'http://127.0.0.1:4040/api/tunnels'
                res = urllib.request.urlopen(local_api).read()
                api = json.loads(res.decode('utf-8'))
                if full:
                    return api['tunnels'][0]
                else:
                    return api['tunnels'][0]['public_url']
            else:
                return 'ngrok is not running'
        except HTTPError as e:
            raise ValueError('An error has occurred while accessing ngrok local api: '+local_api, e)
        except URLError as e:
            raise ValueError('An error has occurred while accessing ngrok local api: '+local_api, e.reason)