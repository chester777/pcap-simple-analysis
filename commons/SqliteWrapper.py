import sqlite3
import logging

from commons.SqliteEnv import *
from GlobalVariable import *

logger = logging.getLogger(LOGGER_NAME)


class SqliteHelper:

    def __init__(self,
                 _sqlite_db_path,
                 _sqlite_init_query_path):

        _conn = sqlite3.connect(_sqlite_db_path,)
        self._db = _conn.cursor()
        self._init(_sqlite_init_query_path)

    def _execute_query(self, sql):

        try:
            self._db.execute(sql)

        except Exception as e:
            logger.error(e)

    @staticmethod
    def _read_sql_file(_file_path):

        _sql = str()
        with open(_file_path, 'r') as f:
            _sql = f.read()
        return _sql

    def _init(self, _sql_file_path):
        pass


class PacketSqliteHelper(SqliteHelper):

    def __init__(self):
        SqliteHelper.__init__(self, PCAP_SQLITE_DB_PATH, PCAP_SQLITE_INIT_QUERY)
