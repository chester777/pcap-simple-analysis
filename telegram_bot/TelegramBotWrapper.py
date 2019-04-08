import logging
import threading
import requests
import time
import json
import asyncio

from GlobalVariable import *
from telegram_bot.TelegramEnv import *

logger = logging.getLogger(LOGGER_NAME)


class TelegramBot:

    def __init__(self, want_update_things=None):

        if want_update_things is not None:
            for update_thing in want_update_things:
                if update_thing == 'file_handle':
                    PLACE_HOLDER_UPDATE_RESULT_DOCUMENT[1] = True

                elif update_thing == 'command':
                    PLACE_HOLDER_UPDATE_RESULT_ENTITIES[1] = True

        self._bot_thread_list = list()
        self._lock = threading.Lock()

        _update_worker_thread = threading.Thread(target=self._run_update_worker)
        _update_worker_thread.start()

    def _run_update_worker(self):
        while True:
            response = requests.get(TELEGRAM_BOT_API_GET_UPDATES_URL)
            updates = json.loads(response.text)

            for update in updates[PLACE_HOLDER_UPDATE_RESULT]:

                # get file to analysis
                if (PLACE_HOLDER_UPDATE_RESULT_DOCUMENT[0] in update
                    and PLACE_HOLDER_UPDATE_RESULT_DOCUMENT[1] is True):
                    with self._lock:
                        asyncio.run(self._get_analysis_file(update))

                # get command
                elif (PLACE_HOLDER_UPDATE_RESULT_ENTITIES[0] in update
                    and PLACE_HOLDER_UPDATE_RESULT_ENTITIES[1] is True):
                    with self._lock:
                        asyncio.run(self._cmd_handler(update))

            time.sleep(TELEGRAM_BOT_API_UPDATE_WAIT_TIME)

    async def _get_analysis_file(self, update):
        pass

    async def _cmd_handler(self, update):
        pass
