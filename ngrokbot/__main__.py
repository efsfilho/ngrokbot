import os
import sys
import pathlib
import logging
from bot import bot
from ngrok import cli

log_dir = './log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'log.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')
handler = logging.FileHandler(log_file)
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)
logging.root.setLevel(logging.INFO)

if __name__ == '__main__':
    token = os.environ['BOT1']
    bot.run(token)
    # cli()