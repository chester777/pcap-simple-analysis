from telegram_bot.TelegramBotWrapper import TelegramBot
from commons.LogWrapper import LogWrapper

class Main:
    def __init__(self):
        LogWrapper('pcap-simple-analysis-logger')
        want_update_things = [
            'file_handle',
            'command'
        ]
        TelegramBot(want_update_things)

if __name__ == '__main__':
    Main()