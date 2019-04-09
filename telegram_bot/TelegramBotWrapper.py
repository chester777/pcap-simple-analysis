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

    def __init__(
            self,
            file_handle=True,
            command_handle=True
         ):

        self._file_handle = file_handle
        self._command_handle = command_handle

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
                if (PLACE_HOLDER_UPDATE_RESULT_DOCUMENT in update[PLACE_HOLDER_MESSAGE]
                    and self._file_handle is True):
                    with self._lock:
                        asyncio.run(self._get_analysis_file(update))

                # get command
                elif (PLACE_HOLDER_UPDATE_RESULT_ENTITIES in update[PLACE_HOLDER_MESSAGE]
                    and self._command_handle is True):
                    with self._lock:
                        asyncio.run(self._cmd_handler(update))

            time.sleep(TELEGRAM_BOT_API_UPDATE_WAIT_TIME)

    async def _get_analysis_file(self, update):
        message = update[PLACE_HOLDER_MESSAGE]
        file_id = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_ID]
        file_name = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_NAME]
        file_detail_url = TELEGRAM_BOT_API_GET_FILE_DETAIL + f'{file_id}'
        file_detail_response = requests.get(file_detail_url)
        file_detail_json = json.loads(file_detail_response.text)
        file_path_telegram_server = file_detail_json[PLACE_HOLDER_FILE_RESULT][PLACE_HOLDER_FILE_PATH]
        file_download_url = TELEGRAM_BOT_API_DOWNLOAD_BASE_URL + file_path_telegram_server

        file_download_response = requests.get(file_download_url)

        file_path_local = f'{PCAP_DOWNLOAD_PATH}/{file_name}'
        with open(file_path_local, 'wb') as fd:
            fd.write(file_download_response.content)

    async def _cmd_handler(self, update):
        pass
