import logging
import logging.handlers
import datetime
import os

from errors.Logger import *
from GlobalVariable import *

LOG_FORMAT = "[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s"

class LogWrapper:

    def __init__(self, name, file=True, display=True, db=False):
        self.name = name
        self.file = file
        self.db = db
        self.display = display
        self.logger = None

        if (self.file or self.db or self.display) is False:
            raise ParamError()

        if os.path.exists(LOG_PATH) is False:
            os.mkdir(LOG_PATH)

        self.logger = self._getLogger()

    def __del__(self):
        del self.name
        del self.db
        del self.logger

    def _getLogger(self):

        if self.logger is None:

            self.logger = logging.getLogger(self.name)

            logFormatter = logging.Formatter(LOG_FORMAT)

            if self.file == True :
                # if you see log in file,
                fileHandler = logging.FileHandler(
                    filename = LOG_PATH + self.name + '-' + datetime.datetime.now().strftime(DATE_FORMAT) + LOG_EXT,
                    encoding = DEFAULT_ENCODING
                )
                fileHandler.setFormatter(logFormatter)
                self.logger.addHandler(fileHandler)

            if self.display == True:
                # if you see log in console at same time,
                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(logFormatter)
                self.logger.addHandler(streamHandler)

            if self.db == True:
                # todo : add database module
                # if you see log in database,
                pass

            return self.logger

        elif self.logger is not None:
            return self.logger

        else:
            return None

    def close(self):
        self.__del__()

    def debug(self, msg):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.setLevel(logging.INFO)
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.setLevel(logging.CRITICAL)
        self.logger.critical(msg)