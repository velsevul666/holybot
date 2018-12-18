#!/usr/bin/env python
#-*- coding: utf-8 -*-
import config
import webscrapping
import birthdayscrap
import json
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
token = config.token
REQUEST_KWARGS = {
    'proxy_url': 'http://195.191.183.169:47238/'
}

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте! Чтобы узнать, какие сегодня праздники наберите /holidays, чтобы узнать, у кого сегодня день рождения - /birthday')



def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Доступны следующие команды: '
                              '/holidays -  узнать праздники сегодня,'
                              '/birthday - узнать, кто родился в этот день,'
                              '/help - посмотреть список команд')

def holidays(bot, update):
    text = webscrapping.results
    text = json.dumps(text,ensure_ascii=False,indent=0)
    update.message.reply_text(text)

def birthday(bot, update):
    text = birthdayscrap.results
    text = json.dumps(text, ensure_ascii=False,indent=0)
    print(text)
    update.message.reply_text(text)

def echo(bot, update):
    update.message.reply_text((update.message.text))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("holidays", holidays))
    dp.add_handler(CommandHandler("birthday", birthday))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()