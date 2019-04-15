import pyshark
from commons.SqliteWrapper import PacketSqliteHelper


class PySharkWrapper:

    def __init__(self):
        self._db_handler = PacketSqliteHelper()

    def result(self, _pcap_id, _pcap_file_path):

        _captures = pyshark.FileCapture(_pcap_file_path)

        for _capture in _captures:
            _packet = self._packet_pre_process(_capture)
            self._packet_after_process(_packet)
        _packet_statistics = self._packet_statistics(_pcap_id)

        return _packet_statistics

    @staticmethod
    def _packet_pre_process(_capture):

        _packet = dict()
        _packet['src_ip'] = _capture.ip.src
        _packet['dst_ip'] = _capture.ip.dst
        _packet['highest_protocol'] = _capture.highest_layer
        _packet['layers'] = list(_.layer_name for _ in _capture.layers)
        _packet['length'] = _capture.length
        return _packet

    def _packet_after_process(self, _packet):
        pass

    def _packet_statistics(self, _pcap_id):
        _packet_statistics = dict()
        return _packet_statistics