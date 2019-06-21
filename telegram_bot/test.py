from telegram_bot.telegram_bot_warpper import TelegramBot
from commons.log_wrapper import MagicLogger
from globals import *

logger = MagicLogger(LOGGER_NAME)


def main():
    logger.info('[*] Start')
    TelegramBot()


if __name__ == '__main__':
    main()
