import os

from errors.telegram_bot import *

TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN', None)

if TELEGRAM_BOT_API_TOKEN is None:
    raise TokenError()

elif not len(TELEGRAM_BOT_API_TOKEN) > 0:
    raise TokenError()

TELEGRAM_BOT_API_UPDATE_WAIT_TIME = 0

TELEGRAM_BOT_API_BASE_URL = 'https://api.telegram.org/bot' + TELEGRAM_BOT_API_TOKEN + '/'
TELEGRAM_BOT_API_DOWNLOAD_BASE_URL = 'https://api.telegram.org/file/bot' + TELEGRAM_BOT_API_TOKEN + '/'
TELEGRAM_BOT_API_GET_UPDATES_URL = TELEGRAM_BOT_API_BASE_URL + 'getUpdates'
TELEGRAM_BOT_API_GET_FILE_DETAIL = TELEGRAM_BOT_API_BASE_URL + 'getFile?file_id='
TELEGRAM_BOT_API_SEND_MESSAGE = TELEGRAM_BOT_API_BASE_URL + 'sendMessage'
TELEGRAM_BOT_API_SEND_PHOTO = TELEGRAM_BOT_API_BASE_URL + 'sendPhoto'

TELEGRAM_BOT_API_CMD_START = '/start'
TELEGRAM_BOT_API_CMD_STOP = '/stop'
TELEGRAM_BOT_API_CMD_HELP = '/help'

PLACE_HOLDER_UPDATE_TIMESTAMP = 'date'
PLACE_HOLDER_UPDATE_ID = 'update_id'
PLACE_HOLDER_MESSAGE = 'message'
PLACE_HOLDER_UPDATE_RESULT = 'result'
PLACE_HOLDER_UPDATE_RESULT_TEXT = 'text'
PLACE_HOLDER_UPDATE_RESULT_DOCUMENT = 'document'
PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_ID = 'file_id'
PLACE_HOLDER_UPDATE_RESULT_DOCUMENT_FILE_NAME = 'file_name'
PLACE_HOLDER_UPDATE_RESULT_ENTITIES = 'entities'

PLACE_HOLDER_FILE_RESULT = 'result'
PLACE_HOLDER_FILE_PATH = 'file_path'

MESSAGE_HELP = "'pcap simple analysis' is a tool for pcap file to analysis packet data simply.\n"
MESSAGE_HELP += 'It provides simple statistics of packet data, and simple network flow by images.\n'
MESSAGE_HELP += 'If you want to analysis pcap file, just drag & drop file in this chat room.\n'
MESSAGE_HELP += 'Good luck your analysis!\n'
