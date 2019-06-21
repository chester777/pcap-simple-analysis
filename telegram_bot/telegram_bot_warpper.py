import logging
import threading
import requests
import time
import json
import random

from globals import *
from telegram_bot.telegram_env import *

from commons.sqlite_wrapper import SQLiteHelper
from commons.db_models import HandledMsg


logger = logging.getLogger(LOGGER_NAME)


class TelegramBot(threading.Thread):

    _handled_update_id_list = list()
    _bot_thread_list = list()
    _thread_lock = threading.Lock()

    def __init__(
            self,
            file_handle=True,
            command_handle=True
         ):

        threading.Thread.__init__(self)

        self._file_handle = file_handle
        self._command_handle = command_handle

        self._init_database()

    def _init_database(self):
        _arg = ArgParser()
        _conf = ConfigParser(_arg.config_path)
        self._db = SQLiteHelper(_conf.db_path)

        with DB_LOCK:
            self._db.session.query(HandledMsg).all()

    def run(self):

        while True:
            response = requests.get(TELEGRAM_BOT_API_GET_UPDATES_URL)
            updates = json.loads(response.text)

            for update in updates[PLACE_HOLDER_UPDATE_RESULT]:

                # check update is in handled update list
                _continue_flag = False
                if update[PLACE_HOLDER_UPDATE_ID] in self._handled_update_id_list:
                    _continue_flag = True
                    break

                if _continue_flag is True:
                    continue

                # get file to analysis
                if (PLACE_HOLDER_UPDATE_RESULT_DOCUMENT in update[PLACE_HOLDER_MESSAGE]
                        and self._file_handle is True):

                    result = self._get_analysis_file(update)

                    if result is not False:
                        self._handled_update_id_list.append(update[PLACE_HOLDER_UPDATE_ID])
                        _temp_msg = HandledMsg(timestamp=int(time.time()),
                                               update_id=update[PLACE_HOLDER_UPDATE_ID])
                        with DB_LOCK:
                            self._db.session.add(_temp_msg)

                # get command
                elif (PLACE_HOLDER_UPDATE_RESULT_ENTITIES in update[PLACE_HOLDER_MESSAGE]
                      and self._command_handle is True):

                        result = self._cmd_handler(update)
                        if result is True:
                            self._handled_update_id_list.append(update[PLACE_HOLDER_UPDATE_ID])

            time.sleep(TELEGRAM_BOT_API_UPDATE_WAIT_TIME)

    @staticmethod
    def _get_analysis_file(update):
        try:
            message = update[PLACE_HOLDER_MESSAGE]
            file_id = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_ID]
            file_name = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_NAME]
            file_detail_url = TELEGRAM_BOT_API_GET_FILE_DETAIL + f'{file_id}'
            file_detail_response = requests.get(file_detail_url)
            file_detail_json = json.loads(file_detail_response.text)
            file_path_telegram_server = file_detail_json[PLACE_HOLDER_FILE_RESULT][PLACE_HOLDER_FILE_PATH]
            file_download_url = TELEGRAM_BOT_API_DOWNLOAD_BASE_URL + file_path_telegram_server

            file_download_response = requests.get(file_download_url)
            file_name_prefix = f'{time.time()}_{random.randrange(1,10000)}'
            file_path_local = f'{PCAP_DOWNLOAD_PATH}/{file_name_prefix}_{file_name}'

            with open(file_path_local, 'wb') as fd:
                fd.write(file_download_response.content)

            return file_path_local

        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def _cmd_handler(update):
        try:
            command = update[PLACE_HOLDER_MESSAGE][PLACE_HOLDER_UPDATE_RESULT_TEXT]

            if command == TELEGRAM_BOT_API_CMD_HELP:
                params = dict(
                    chat_id=update[PLACE_HOLDER_MESSAGE]['chat']['id'],
                    text=MESSAGE_HELP
                )

                response = requests.get(TELEGRAM_BOT_API_SEND_MESSAGE, params=params)
                if response.status_code is 200:
                    return True

            elif command == TELEGRAM_BOT_API_CMD_START:
                pass
            elif command == TELEGRAM_BOT_API_CMD_STOP:
                pass

            return True
        except Exception as e:
            logger.error(e)
            return False
