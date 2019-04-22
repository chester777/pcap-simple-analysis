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

        _result_list = self._db_handler.select_by_pcap_id(_pcap_id)

        for _result in _result_list:

            # total IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['total'].items():
                if _result['src_ip'] == _ip or _result['dst_ip'] == _ip:
                    _packet_statistics['ip_frequency']['total'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if total dictionary is empty
                _packet_statistics['ip_frequency']['total'][_result['src_ip']] = 1
                _packet_statistics['ip_frequency']['total'][_result['dst_ip']] = 1

            # source IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['src_ip'].items():
                if _result['src_ip'] == _ip:
                    _packet_statistics['ip_frequency']['src_ip'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if source dictionary is empty
                _packet_statistics['ip_frequency']['src_ip'][_result['src_ip']] = 1

            # destination IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['dst_ip'].items():
                if _result['dst_ip'] == _ip:
                    _packet_statistics['ip_frequency']['dst_ip'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if destination dictionary is empty
                _packet_statistics['ip_frequency']['dst_ip'][_result['dst_ip']] = 1


        return _packet_statistics
