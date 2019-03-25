from telegram_bot.TelegramBotWrapper import TelegramBotWrapper
from commons.LogWrapper import LogWrapper


class Main:
    def __init__(self):
        LogWrapper('pcap-simple-analysis-logger')
        TelegramBotWrapper()


if __name__ == '__main__':
    Main()
