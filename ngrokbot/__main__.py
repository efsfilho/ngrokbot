import os
import sys
import logging
from bot import bot
from ngrok import cli

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')
handler = logging.FileHandler('./log/log.log')
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)

if __name__ == '__main__':
    token = os.environ['BOT1']
    bot.run(token)
    # cli()