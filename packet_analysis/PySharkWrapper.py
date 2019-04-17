import pyshark
from commons.SqliteWrapper import PacketSqliteHelper


class PySharkWrapper:

    def __init__(self):
        self._db_handler = PacketSqliteHelper()

    def result(self, _pcap_id, _pcap_file_path):

        _captures = pyshark.FileCapture(_pcap_file_path)

        for _capture in _captures:
            _packet = self._packet_pre_process(_pcap_id, _capture)
            self._packet_after_process(_packet)
        _packet_statistics = self._packet_statistics(_pcap_id)

        return _packet_statistics

    @staticmethod
    def _packet_pre_process(_pcap_id, _capture):

        _packet = dict()
        _packet['pcap_id'] = _pcap_id
        _packet['packet_no'] = _capture.number
        _packet['src_ip'] = _capture.ip.src
        _packet['dst_ip'] = _capture.ip.dst
        _packet['highest_protocol'] = _capture.highest_layer
        _packet['layers'] = ','.join(list(_.layer_name for _ in _capture.layers))
        _packet['packet_length'] = _capture.length
        return _packet

    def _packet_after_process(self, _packet):
        _result = self._db_handler.insert_into_packet_data(_packet)

    def _packet_statistics(self, _pcap_id):
        _packet_statistics = dict(
            ip_frequency=dict(
                total=dict(),
                src_ip=dict(),
                dst_ip=dict()
            ),
            layers_frequency=dict(),
            highest_layer_frequency=dict(),
            length_rate=dict()
        )

        _ip_list = dict()

        _result_list = self._db_handler.select_by_pcap_id(_pcap_id)

        for _result in _result_list:
            pass

        return _packet_statistics