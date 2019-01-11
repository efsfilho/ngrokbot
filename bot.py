#!/usr/bin/python3

import os
import telegram
import logging
import json
import time
import subprocess

from urllib import request as req
from telegram.ext import CommandHandler
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class NgrokManager:

    def __init__(self):
        # ngrok e parametros
        ngrok = ''
        protocol = ''
        port = ''
        self.ngrokParams = [ngrok, protocol, port]
        self.process = None

    def __terminated(self):
        p = self.process
        if p == None or p.poll() == None:
            return True
        else:
            return False

    def start(self):
        # TODO verificar processos existentes
        if self.__terminated():
            self.process = subprocess.Popen(self.ngrok, stdout=subprocess.PIPE, shell=False)

    def stop(self):
        if not self.__terminated():
            self.process.terminate()
            self.process = None

    def getInfo(self, full=False):
        # TODO validacao
        if not self.__terminated():
            try:
                res = req.urlopen('http://localhost:4040/api/tunnels').read()
                api = json.loads(res.decode('utf-8'))
                if full:
                    return api['tunnels'][0]
                else:
                    return api['tunnels'][0]['public_url']
            except:
                return 'Erro ao carregar informações.'
        else:
            return 'Ngrok não iniciado'
        
updater = Updater(token='')
dispatcher = updater.dispatcher

nkp = NgrokManager()

def eco(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='eco')

def status(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=nkp.getInfo(True))

def start(bot, update):
    nkp.start()
    bot.send_message(chat_id=update.message.chat_id, text='start')

def stop(bot, update):
    nkp.stop()
    bot.send_message(chat_id=update.message.chat_id, text='stop')

def info(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=nkp.getInfo())

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))
dispatcher.add_handler(CommandHandler('info', info))

updater.start_polling() 
