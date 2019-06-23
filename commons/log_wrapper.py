import logging
import logging.handlers
import datetime
import os

from errors.log_wrapper import ParamError
from commons.globals import *
from commons.arg_parser import ArgParser
from commons.config_parser import ConfigParser


class MagicLogger:

    def __init__(self,
                 logger_name,
                 log_file_name=None,
                 file_out=True,
                 display_out=True,
                 db_out=False):

        self._args = ArgParser()
        self._conf = ConfigParser(self._args.config_path)
        self._logger_name = logger_name

        if log_file_name is None:
            self._log_file_name = logger_name
        else:
            self._log_file_name = log_file_name

        self._file_out = file_out
        self._db_out = db_out
        self._display_out = display_out

        if (self._file_out or self._db_out or self._display_out) is False:
            raise ParamError()

        if os.path.exists(self._conf.log_path) is False:
            os.makedirs(self._conf.log_path)

        self._get_logger()

    def _get_logger(self):

        self._logger = logging.getLogger(self._logger_name)

        _log_formatter = logging.Formatter(LOG_FORMAT)

        if self._file_out is True:
            # if you see log in file,

            _log_date = datetime.datetime.now().strftime(DATE_FORMAT)
            _log_file_path = '%s/%s-%s.%s' % (self._conf.log_path,
                                              self._log_file_name,
                                              _log_date,
                                              LOG_EXT)

            _file_handler = logging.FileHandler(
                filename=_log_file_path,
                encoding=DEFAULT_CHARSET
            )
            _file_handler.setFormatter(_log_formatter)
            self._logger.addHandler(_file_handler)

        if self._display_out is True:
            # if you see log in console at same time,
            _stream_handler = logging.StreamHandler()
            _stream_handler.setFormatter(_log_formatter)
            self._logger.addHandler(_stream_handler)

        if self._db_out is True:
            # todo : add database module
            # if you see log in database,
            pass

    def error(self, msg):
        self._logger.setLevel(logging.ERROR)
        self._logger.error(msg)

    def info(self, msg):
        self._logger.setLevel(logging.INFO)
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.setLevel(logging.WARNING)
        self._logger.warning(msg)

    def debug(self, msg):
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug(msg)

    def critical(self, msg):
        self._logger.setLevel(logging.CRITICAL)
        self._logger.critical(msg)
