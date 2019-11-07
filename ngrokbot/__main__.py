import os
import sys
import logging
from bot import bot
from ngrok import cli
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')

def config_log():
    # Config log
    log_dir = './log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'log.log')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s > %(funcName)s: %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)
    logging.root.setLevel(logging.INFO)

def main():
    # Telegram token
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)

    telegram_token = os.getenv('TELEGRAM_TOKEN')
    if telegram_token is None:
        logging.error('Telegram token not found')
        exit()
    bot.run(telegram_token)

if __name__ == '__main__':
    config_log()
    main()
    # cli()