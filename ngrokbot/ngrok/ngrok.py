import os
import json
import time
import logging
import pathlib
import zipfile
import tempfile
import subprocess
from .util import *

logger = logging.getLogger()

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

        try:
            platform = get_platform()
            if platform['os'] == 'Linux':
                file_name = 'ngrok'
            else:
                file_name = 'ngrok.exe'

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

                print('Platform.............:',platform['os'], platform['arch'])

                # downloads ngrok zip
                download_file(ngrok_zip_path)

                print(f'Extracting ngrok from: {ngrok_zip_path}')

                zip_file = zipfile.ZipFile(ngrok_zip_path, 'r')
                zip_file.extractall(ngrok_instalation_path)
                zip_file.close()

                os.chmod(ngrok_path, 0o755)

                if ngrok_path.is_file():
                    if platform['os'] == 'Windows':
                        return str(ngrok_path)
                    else:
                        return ngrok_path
                else:
                    return None

        except ValueError as valueError:
            logger.error(valueError)

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

    def started(self):
        return self.__is_ngrok_running()

    def get_ngrok(self):
        """
        Returns true if ngrok is installed
        """
        print('NgrokManager starting...')
        self.__ngrok_executable = self.__install_ngrok()

        if self.__ngrok_executable != None:
            print(f'Ngrok executable.....: {self.__ngrok_executable}\n')
            return True
        else:
            return False

    def start(self, arg_list=None):
        if not self.__is_ngrok_running():
            msg = ''
            try:
                if self.__ngrok_executable is None:
                    self.__ngrok_executable = self.__install_ngrok()
                    if self.__ngrok_executable is None:
                        raise Exception('It was not possible to get ngrok executable path')

                token = '--authtoken=asd'

                if arg_list is None or len(arg_list) < 2 :
                    # args = ['tcp', '22']
                    args = []
                else:
                    args = arg_list
                
                args.insert(0, self.__ngrok_executable)

                self.__ngrok_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                time.sleep(2) # wait ngrok digest

                if self.__ngrok_process.poll() is None:
                    args.remove(args[0])
                    args_str = ' '.join(args)
                    logger.info(f'PID: {self.__ngrok_process.pid} COMMAND {self.__ngrok_executable} {args_str}')
                    url = self.get_info()
                    logger.info(f'URL: {url}')
                    msg = url
                else:
                    for line in self.__ngrok_process.stdout:
                        msg += line.decode('utf-8')

            except Exception as exception:
                logger.error(exception)
                msg = 'It was not possible to execute ngrok'
            finally:
                return msg

    def stop(self):
        msg = ''
        if self.__is_ngrok_running():
            self.__ngrok_process.terminate()
            self.__ngrok_process = None
            if not self.__is_ngrok_running():
                msg = 'ngrok stoped'
            else:
                # TODO force to kill it
                msg = 'It was not possible to stop ngrok'
        self.__started = False
        return msg

    def get_stdout(self):
        msg = ''
        if isinstance(self.__ngrok_process, subprocess.Popen):
            # if self.__ngrok_process.poll() is None:
            #     msg = self.__ngrok_process.communicate()[0]
            for line in self.__ngrok_process.stdout:
                msg += line.decode('utf-8')
        return msg

    def get_info(self, full=False):
        msg = ''
        try:
            if self.__is_ngrok_running():
                local_api = 'http://127.0.0.1:4040/api/tunnels'
                res = urllib.request.urlopen(local_api).read()
                api = json.loads(res.decode('utf-8'))
                if full:
                    msg = api['tunnels'][0]
                else:
                    msg = api['tunnels'][0]['public_url']
            else:
                msg = 'ngrok is not running'
        except HTTPError as exception:
            logger.error(f'An error has occurred while accessing ngrok local api: {local_api} {exception}')
            msg = 'It was not possible to get any info from ngrok'
        except URLError as exception:
            logger.error(f'An error has occurred while accessing ngrok local api: {local_api} {exception.reason}')
            msg = 'It was not possible to get any info from ngrok'
        finally:
            return msg
