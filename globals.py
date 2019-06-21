from commons.arg_parser import ArgParser
from commons.config_parser import ConfigParser
from threading import Lock

"""
set global variable in this module.
"""

_arg = ArgParser()
_conf = ConfigParser(_arg.config_path)

# Project Name
PROJECT_NAME = 'pcap-simple-analysis'

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

PCAP_DOWNLOAD_PATH = _conf.pcap_file_path

# variables about database
DB_LOCK = Lock()
