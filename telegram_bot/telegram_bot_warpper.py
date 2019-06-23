import logging
import threading
import requests
import time
import json
import random

from commons.globals import *
from telegram_bot.telegram_env import *

from commons.sqlite_wrapper import SQLiteHelper
from commons.db_models import HandledMsg


logger = logging.getLogger(LOGGER_NAME)


class TelegramInputBot(threading.Thread):

    _handled_update_id_list = list()
    _bot_thread_list = list()
    _update_lock = threading.Lock()

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

        if os.path.exists(_conf.db_dir_path) is False:
            os.makedirs(_conf.db_dir_path)

        _db_path = '/'.join([ROOT_PATH, _conf.db_path])
        self._db = SQLiteHelper(_db_path)

        for _msg in self._db.session.query(HandledMsg).all():
            with self._update_lock:
                self._handled_update_id_list.append(_msg.update_id)

    def run(self):

        while True:
            response = requests.get(TELEGRAM_BOT_API_GET_UPDATES_URL)
            updates = json.loads(response.text)

            for update in updates[PLACE_HOLDER_UPDATE_RESULT]:

                # check update is in handled update list
                if update[PLACE_HOLDER_UPDATE_ID] in self._handled_update_id_list:
                    break

                if ((PLACE_HOLDER_UPDATE_RESULT_DOCUMENT in update[PLACE_HOLDER_MESSAGE]
                    or PLACE_HOLDER_UPDATE_RESULT_ENTITIES in update[PLACE_HOLDER_MESSAGE])
                        and self._file_handle is True):

                    result = False

                    # get file to analysis
                    if PLACE_HOLDER_UPDATE_RESULT_DOCUMENT in update[PLACE_HOLDER_MESSAGE]:
                        result = dict(
                            chat_id=update[PLACE_HOLDER_MESSAGE]['chat']['id'],
                            pcap_file_path=self._get_analysis_file(update)
                        )

                    # get command
                    elif PLACE_HOLDER_UPDATE_RESULT_ENTITIES in update[PLACE_HOLDER_MESSAGE]:
                        result = dict(
                            chat_id=update[PLACE_HOLDER_MESSAGE]['chat']['id'],
                            cmd=self._cmd_handler(update)
                        )

                    if result is not False:
                        _temp_msg = HandledMsg(timestamp=int(time.time()),
                                               update_id=update[PLACE_HOLDER_UPDATE_ID])

                        with DB_LOCK:
                            self._db.session.add(_temp_msg)
                            self._db.session.commit()

                        with self._update_lock:
                            self._handled_update_id_list.append(update[PLACE_HOLDER_UPDATE_ID])

                        with INPUT_JOB_QUEUE_LOCK:
                            INPUT_JOB_QUEUE.put(result)

            time.sleep(TELEGRAM_BOT_API_UPDATE_WAIT_TIME)

    @staticmethod
    def _get_analysis_file(update):
        try:
            message = update[PLACE_HOLDER_MESSAGE]
            file_id = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_ID]
            file_name = message[PLACE_HOLDER_UPDATE_RESULT_DOCUMENT][PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_NAME]
            file_detail_url = TELEGRAM_BOT_API_GET_FILE_DETAIL + file_id
            file_detail_response = requests.get(file_detail_url)
            file_detail_json = json.loads(file_detail_response.text)
            file_path_telegram_server = file_detail_json[PLACE_HOLDER_FILE_RESULT][PLACE_HOLDER_FILE_PATH]
            file_download_url = TELEGRAM_BOT_API_DOWNLOAD_BASE_URL + file_path_telegram_server

            file_download_response = requests.get(file_download_url)
            file_name_prefix = '%s_%s' % (time.time(), random.randrange(1, 10000))

            file_path_local = '%s/%s_%s' % (PCAP_DOWNLOAD_PATH, file_name_prefix, file_name)

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


class TelegramOutputBot(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._init_database()

    def _init_database(self):
        _arg = ArgParser()
        _conf = ConfigParser(_arg.config_path)

        if os.path.exists(_conf.db_dir_path) is False:
            os.makedirs(_conf.db_dir_path)

        _db_path = '/'.join([ROOT_PATH, _conf.db_path])
        self._db = SQLiteHelper(_db_path)

    def run(self):

        while True:

            with OUTPUT_JOB_QUEUE_LOCK:
                if OUTPUT_JOB_QUEUE.empty() is True:
                    continue

            with OUTPUT_JOB_QUEUE_LOCK:
                _job = OUTPUT_JOB_QUEUE.get()

                if _job['type'] == 'packet_analysis_result':

                    _files = dict(
                        photo=open(_job['image_path'], 'rb'),
                    )

                    _data = dict(
                        chat_id=_job['chat_id'],
                    )

                    _msg = dict(
                        chat_id=_job['chat_id'],
                        text=_job['pcap_statistics'],
                    )
                    _response = requests.post(TELEGRAM_BOT_API_SEND_PHOTO, files=_files, data=_data)
                    if _response.status_code is 200:
                        logger.info('Send photo success')
                    else:
                        logger.info('Send photo fail')

                    _response = requests.get(TELEGRAM_BOT_API_SEND_MESSAGE, params=_msg)
                    if _response.status_code is 200:
                        logger.info('Send message success')
                    else:
                        logger.info('Send message fail')

                elif _job['type'] == 'cmd_result':
                    _msg = dict(
                        chat_id=_job['chat_id'],
                        text=_job['cmd_result'],
                    )
                    _response = requests.get(TELEGRAM_BOT_API_SEND_MESSAGE, params=_msg)
                    if _response.status_code is 200:
                        logger.info('Send message success')
                    else:
                        logger.info('Send message fail')
