import re
import json
import logging
import telegram
from ngrok import NgrokManager
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logger = logging.getLogger()

ngrok = NgrokManager()

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

def url(update, context):
    info(update, context, False)

def stop(update, context):
    ngrok.stop()
    update.message.reply_text('signal to stop sent')
    
def echo(update, context):
    update.message.reply_text(f'echo {update.message.text}')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s"', context.error)

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
    updater.idle()
