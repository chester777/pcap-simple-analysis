from commons.log_wrapper import MagicLogger
from telegram_bot.telegram_bot_warpper import TelegramBot
from globals import *

logger = MagicLogger(PROJECT_NAME)


def main():
    try:
        logger.info(f'[+] Start {PROJECT_NAME}')

        

        while True:
            pass

    except (KeyboardInterrupt, SystemExit):
        logger.info(f'[-] Stop {PROJECT_NAME}')

if __name__ == '__main__':
    main()