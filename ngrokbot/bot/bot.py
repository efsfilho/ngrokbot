import os
import re
import json
import logging
import telegram
from pathlib import Path
from functools import wraps
from ngrok import NgrokManager
from dotenv import load_dotenv, set_key
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logger = logging.getLogger()

ngrok = NgrokManager()

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

user_id_list = []
username_list = []

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user = update.effective_user
        is_id_allow = user.id in user_list:
        is_user_allow = user.username in user_list:
        if not is_id_allow or not is_user_allow
            logging.info('Unauthorized access denied for User:{}.'.format(user))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def start(update, context):
    msg = ' '
    try:
        text = update.message.text
        text = re.sub(r'\/ngrok','', text)
        if ngrok.started():
            msg = 'ngrok is already runnning'
        else:
            text = text[1:]
            args = text.split(' ')
            msg = f'```{ngrok.start(args)}```'
    except Exception as exception:
        logger.error(exception)
        msg = 'It was not possible to start ngrok'
    finally:
        update.message.reply_text(msg, parse_mode=telegram.ParseMode.MARKDOWN)

@restricted
def info(update, context, full=True):
    if ngrok.started():
        try:
            info = ''
            info = ngrok.get_info(full)
            info = f'```{json.dumps(info, indent=2)}```'
            update.message.reply_text(info, parse_mode=telegram.ParseMode.MARKDOWN)
        except Exception as exception:
            logger.error(exception)
            update.message.reply_text('It was not possible to get ngrok info.')
    else:
        update.message.reply_text('ngrok is not running, start it first with /ngrok')

@restricted
def url(update, context):
    info(update, context, False)

@restricted
def stop(update, context):
    ngrok.stop()
    update.message.reply_text('signal to stop sent')

def echo(update, context):
    update.message.reply_text(f'echo {update.message.text}')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s"', context.error)

# def update_users():
#     import random
#     r = random.randint(0, 9999)
#     print(r)
#     set_key(dotenv_path=env_path, key_to_set='TEST', value_to_set=str(r))

def run(token=None):
    ngrok.get_ngrok()

    updater = Updater(token, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler('ngrok', start))
    disp.add_handler(CommandHandler('info', info))
    disp.add_handler(CommandHandler('url', url))
    disp.add_handler(CommandHandler('stop', stop))
    disp.add_handler(CommandHandler('echo', echo))
    disp.add_handler(MessageHandler(Filters.text, echo))
    disp.add_error_handler(error)

    updater.start_polling()
    logger.info('Bot started')
    user_id = os.getenv('USER_ID')
    if user_id is None:
        logging.warn('User id not found, no one will be able to use the bot')
    updater.idle()
