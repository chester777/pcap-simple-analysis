import telegram
from telegram.ext import Updater

API_TOKEN = '892925774:AAH-w0XBPve7nIuJhVtCeSpNGyXO4NQHDyo'

class TelegramBotWrapper:

    def __init__(self):
        self.updater = Updater(token=API_TOKEN, user_context=True)
        self.dispatcher = updater.dispatcher

    def start(self):
        pass
        

        #updates = bot.getUpdates()

        #for update in updates:
        #    print(update.message)