import os
import queue
from threading import Lock

from commons.arg_parser import ArgParser
from commons.config_parser import ConfigParser

"""
set global variable in this module.
"""

_arg = ArgParser()
_conf = ConfigParser(_arg.config_path)

# Project Information
PROJECT_NAME = 'pcap-simple-analysis'
ROOT_PATH = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])

# Default character set
DEFAULT_CHARSET = 'utf-8'

# Default date format
DATE_FORMAT = '%Y-%m-%d'

# Default datetime format
DATETIME_FORMAT = 'yyyy-mm-dd hh:MM:ss'

# variables about logger
LOGGER_NAME = 'pcap-simple-analysis'
LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s pid=%(process)d > %(message)s'
LOG_EXT = 'log'

# variables about environment
PCAP_DOWNLOAD_PATH = './pcap_files'

# variables about database
DB_LOCK = Lock()

# variables about job queue
INPUT_JOB_QUEUE = queue.Queue()
OUTPUT_JOB_QUEUE = queue.Queue()

INPUT_JOB_QUEUE_LOCK = Lock()
OUTPUT_JOB_QUEUE_LOCK = Lock()
