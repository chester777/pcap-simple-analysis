from commons.log_wrapper import MagicLogger
from commons.globals import *
from telegram_bot.telegram_bot_warpper import TelegramInputBot, TelegramOutputBot
from packet_analysis.job_worker import JobWorker

logger = MagicLogger(PROJECT_NAME)


def main():
    try:
        logger.info('[+] Start %s' % PROJECT_NAME)

        telegram_input_bot = TelegramInputBot()
        telegram_output_bot = TelegramOutputBot()
        job_worker = JobWorker()

        telegram_input_bot.start()
        telegram_output_bot.start()
        job_worker.start()

        while True:
            pass

    except (KeyboardInterrupt, SystemExit):
        logger.info('[+] Stop %s' % PROJECT_NAME)


if __name__ == '__main__':
    main()