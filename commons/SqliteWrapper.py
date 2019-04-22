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
                _result = self._db.execute(_sql)
            else:
                _result = self._db.execute(_sql, _sql_param)

            self._conn.commit()
            return _result

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

    def select_by_pcap_id(self, _pcap_id):

        _sql = self._read_sql_file(PCAP_SELECT_BY_PCAP_ID_QUERY_PATH)
        _valid_pcap_id = self._check_valid_data(_pcap_id)

        _query_param = dict(
            pcap_id=_valid_pcap_id
        )

        _result_list = self._execute_query(_sql, _query_param)

        for _result in _result_list.fetchall():
            _result_dict = dict(
                pcap_id=_result[0],
                packet_no=_result[1],
                src_ip=_result[2],
                dst_ip=_result[3],
                highest_protocol=_result[4],
                layers=_result[5].split(','),
                packet_length=_result[6]
            )
            yield _result_dict
