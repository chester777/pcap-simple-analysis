import sqlite3
import logging

from commons.SqliteEnv import *
from GlobalVariable import *

logger = logging.getLogger(LOGGER_NAME)


class SqliteHelper:

    def __init__(self,
                 _sqlite_db_path,
                 _sqlite_init_query_path):

        self._conn = sqlite3.connect(_sqlite_db_path,)
        self._db = self._conn.cursor()
        self._init(_sqlite_init_query_path)

    def _execute_query(self, _sql, _sql_param=None):

        try:
            if _sql_param is None:
                self._db.execute(_sql)
            else:
                self._db.execute(_sql, _sql_param)

            self._conn.commit()
            return True

        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def _read_sql_file(_file_path):

        _sql = str()
        with open(_file_path, 'r') as f:
            _sql = f.read()
        return _sql

    def _init(self, _sql_file_path):
        _sql = self._read_sql_file(_sql_file_path)
        _result = self._execute_query(_sql)

    @staticmethod
    def _check_valid_data(_packet_info):
        _result = _packet_info
        return _result


class PacketSqliteHelper(SqliteHelper):

    def __init__(self):

        SqliteHelper.__init__(self, PCAP_SQLITE_DB_PATH, PCAP_SQLITE_INIT_QUERY_PATH)

    def insert_into_packet_data(self, _packet_info):

        _sql = self._read_sql_file(PCAP_INSERT_INTO_PACKET_DATA_QUERY_PATH)
        _valid_packet_info = self._check_valid_data(_packet_info)
        _result = self._execute_query(_sql, _valid_packet_info)

        return _result

