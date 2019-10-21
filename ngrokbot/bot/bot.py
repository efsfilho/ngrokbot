import re
import json
import logging
from ngrok import NgrokManager
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ngrok = NgrokManager()

def start(update, context):
    text = update.message.text
    text = re.sub(r'\/ngrok','', text)
    msg = ' '
    if ngrok.started():
        msg = 'Ngrok already Runnning.'
    else:
        try:
            # if len(text) > 1:
            text = text[1:]
            args = text.split(' ')
            ngrok.start(args)
            if ngrok.started():
                msg = 'ngrok started'
                # TODO better msg return
        except Exception as exception:
            logger.error(f'start(): {exception}')
            msg = 'It was not possible to start ngrok.'

    # bot.send_message(chat_id=update.message.chat_id, text=msg)
    update.message.reply_text(msg)


def status(update, context):
    if ngrok.started():
        try:
            info = ''
            info = ngrok.get_info(True)
            info = f'```{json.dumps(info, indent=2)}```'
            update.message.reply_text(info, parse_mode=telegram.ParseMode.MARKDOWN)
        except Exception as exception:
            logger.error(f'status(): {exception}')
            update.message.reply_text('It was not possible to get ngrok info.')
    else:
        update.message.reply_text('Ngrok is not running, start it first with /ngrok')

def url(update, context):
    if ngrok.started():
        try:
            info = ''
            info = f'```{ngrok.get_info()}```'
            update.message.reply_text(info, parse_mode=telegram.ParseMode.MARKDOWN)
        except Exception as exception:
            logger.error(f'status(): {exception}')
            update.message.reply_text('It was not possible to get ngrok info.')
    else:
        update.message.reply_text('Ngrok is not running, start it first with /ngrok')

def stop(update, context):
    ngrok.stop()
    update.message.reply_text('signal to stop sent')
    
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Error "%s"', context.error)

def run(token=None):
    ngrok.get_ngrok()
    updater = Updater(token, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler('ngrok', start))
    disp.add_handler(CommandHandler('status', status))
    disp.add_handler(CommandHandler('url', url))
    disp.add_handler(CommandHandler('stop', stop))
    disp.add_handler(MessageHandler(Filters.text, echo))

    disp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
