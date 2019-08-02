#!/usr/bin/python3

import os
import telegram
import logging

from telegram.ext import CommandHandler
from telegram.ext import Updater
from ngrok.app import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['b1']

updater = Updater(token=token)
dispatcher = updater.dispatcher

def eco(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='eco123')

def start(bot, update):
    # execute(bot.)
    # print(update.message.)
    bot.send_message(chat_id=update.message.chat_id, text='eco123')

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling() 
