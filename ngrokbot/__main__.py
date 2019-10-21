import os
from bot import bot

if __name__ == '__main__':
    token = os.environ['BOT1']
    bot.run(token)