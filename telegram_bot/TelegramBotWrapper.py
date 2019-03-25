import os
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

from errors.TelegramBot import *

TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN', None)

if TELEGRAM_BOT_API_TOKEN is None:
    raise TokenError()

elif not len(TELEGRAM_BOT_API_TOKEN) > 0:
    raise TokenError()

logger = logging.getLogger('pcap-simple-analysis-logger')


class TelegramBotWrapper:

    def __init__(self):
        updater = Updater(token=TELEGRAM_BOT_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', self.start_cmd)
        msg_handler = MessageHandler(Filters.all, self.msg_handler)

        dispatcher.add_handler(msg_handler)
        dispatcher.add_handler(start_handler)
        dispatcher.add_error_handler(self.error_handler)

        logger.info('* Start Telegram Bot')

        updater.start_polling()
        updater.idle()

    @staticmethod
    def start_cmd(update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="I'm a bot, please talk to me!"
        )

    @staticmethod
    def msg_handler(update, context):
        try:
            message = 'Unknown Message'
            if update.message.document is not None:
                # file handling
                file_id = update.message.document.file_id
                file_name = update.message.document.file_name
                new_file = context.bot.get_file(file_id)
                new_file.download(file_name)

            else:
                # text handling
                message = update.message.text

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=message
            )

        except Exception as e:
            print(e)

    @staticmethod
    def error_handler(update, context):
        pass
