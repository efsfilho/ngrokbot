#!/usr/bin/python3

import os
import re
import json
import logging
import telegram

from telegram.ext import CommandHandler
from telegram.ext import Updater
from ngrok import app as ngrok

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['b1']

updater = Updater(token=token)
dispatcher = updater.dispatcher

# def command_filter(text):
#     # re_commands = [r'\//start']
#     # for commands in re_commands:
#     return re.sub(r'\\','', text)

def eco(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='eco')

def start(bot, update):
    text = update.message.text
    cmd = re.sub(r'\/start','', text)
    msg = ''
    if ngrok.is_running():
        msg = 'Ngrok already Runnning.'
    else:
        ngrok.execute(cmd[1:])
        # ngrok.execute('http 2500')
        msg = 'Starting'

    bot.send_message(chat_id=update.message.chat_id, text=msg)

def stop(bot, update):
    ngrok.stop()
    bot.send_message(chat_id=update.message.chat_id, text='stop')

def status(bot, update):
    info = ''
    try:
        if ngrok.is_running():
            info = ngrok.get_info(True)
            info = '```'+json.dumps(info, indent=2)+'```'
        else:
            info = 'Ngrok is not running, start it first with /start'
    except:
        # TODO except handle
        info = 'It was not possible to get ngrok info.'

    bot.send_message(chat_id=update.message.chat_id,
        text=info,
        parse_mode=telegram.ParseMode.MARKDOWN)

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))
dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling() 
