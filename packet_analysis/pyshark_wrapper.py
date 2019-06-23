import pyshark
import os
import time

from commons.globals import ROOT_PATH
from commons.config_parser import ConfigParser
from commons.arg_parser import ArgParser
from commons.sqlite_wrapper import SQLiteHelper
from commons.db_models import PacketData


class PySharkWrapper:

    def __init__(self):
        _arg = ArgParser()
        _conf = ConfigParser(_arg.config_path)

        if os.path.exists(_conf.db_dir_path) is False:
            os.makedirs(_conf.db_dir_path)

        _db_path = '/'.join([ROOT_PATH, _conf.db_path])
        self._db = SQLiteHelper(_db_path)

    def result(self, _pcap_file_path):

        _captures = pyshark.FileCapture(_pcap_file_path)

        _pcap_id = int(time.time())
        for _capture in _captures:
            _packet = self._packet_pre_process(_pcap_id, _capture)
            self._packet_after_process(_packet)
        self._db.session.commit()

        if _pcap_id is not None:
            _statistics_result = self._packet_statistics(_pcap_id)
            return _pcap_id, _statistics_result

    @staticmethod
    def _packet_pre_process(_pcap_id, _capture):
        _packet = PacketData(
            pcap_id=_pcap_id,
            packet_num=_capture.number,
            src_ip=_capture.ip.src,
            dst_ip=_capture.ip.dst,
            highest_protocol=_capture.highest_layer,
            layers=','.join(list(_.layer_name for _ in _capture.layers)),
            packet_length=_capture.length
        )
        return _packet

    def _packet_after_process(self, _packet):
        self._db.session.add(_packet)

    def _packet_statistics(self, _pcap_id):
        _packet_statistics = dict(
            ip_frequency=dict(
                total=dict(),
                src_ip=dict(),
                dst_ip=dict()
            ),
            layers_frequency=list(),
            highest_protocol_frequency=dict(),
            length_rate=dict(
                len_1_to_10=0,
                len_10_to_100=0,
                len_100_to_200=0,
                len_200_to_300=0,
                len_300_to_400=0,
                len_400_to_500=0,
                len_500_to_600=0,
                len_600_to_700=0,
                len_700_to_800=0,
                len_800_to_900=0,
                len_900_to_1000=0,
                len_1000_to_2000=0,
                len_2000_to_3000=0,
                len_3000_to_4000=0,
                len_4000_to_5000=0,
                len_5000_to_6000=0,
                len_6000_to_7000=0,
                len_7000_to_8000=0,
                len_8000_to_9000=0,
                len_9000_to_10000=0,
                len_10000_over=0
            )
        )

        _result_list = self._db.session.query(PacketData).filter_by(pcap_id=_pcap_id).all()

        for _packet in _result_list:

            # total IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['total'].items():
                if _packet.src_ip == _ip or _packet.dst_ip == _ip:
                    _packet_statistics['ip_frequency']['total'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if total dictionary is empty
                _packet_statistics['ip_frequency']['total'][_packet.src_ip] = 1
                _packet_statistics['ip_frequency']['total'][_packet.dst_ip] = 1

            # source IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['src_ip'].items():
                if _packet.src_ip == _ip:
                    _packet_statistics['ip_frequency']['src_ip'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if source dictionary is empty
                _packet_statistics['ip_frequency']['src_ip'][_packet.src_ip] = 1

            # destination IP count
            _iterate_flag = False
            for _ip, _count in _packet_statistics['ip_frequency']['dst_ip'].items():
                if _packet.dst_ip == _ip:
                    _packet_statistics['ip_frequency']['dst_ip'][_ip] = _count + 1
                    _iterate_flag = True

            if _iterate_flag is False:
                # if destination dictionary is empty
                _packet_statistics['ip_frequency']['dst_ip'][_packet.dst_ip] = 1

            # layer frequency count
            _layers = _packet.layers.split(',')

            for _layer in _layers:

                _iterate_flag = False
                _index = 0
                for _layer_info in _packet_statistics['layers_frequency']:
                    if _layer in _layer_info:
                        _packet_statistics['layers_frequency'][_index][_layer] += 1
                        _iterate_flag = True
                    _index += 1

                if _iterate_flag is False:
                    _new_dict = dict()
                    _new_dict[_layer] = 1
                    _packet_statistics['layers_frequency'].append(_new_dict)

            # highest protocol frequency count
            if _packet.highest_protocol in _packet_statistics['highest_protocol_frequency']:
                _packet_statistics['highest_protocol_frequency'][_packet.highest_protocol] += 1
            else:
                _packet_statistics['highest_protocol_frequency'][_packet.highest_protocol] = 1

            # packet length rate
            if 0 <= _packet.packet_length < 10:
                _packet_statistics['length_rate']['len_1_to_10'] += 1

            elif 10 <= _packet.packet_length < 100:
                _packet_statistics['length_rate']['len_10_to_100'] += 1

            elif 100 <= _packet.packet_length < 200:
                _packet_statistics['length_rate']['len_100_to_200'] += 1

            elif 200 <= _packet.packet_length < 300:
                _packet_statistics['length_rate']['len_200_to_300'] += 1

            elif 300 <= _packet.packet_length < 400:
                _packet_statistics['length_rate']['len_300_to_400'] += 1

            elif 400 <= _packet.packet_length < 500:
                _packet_statistics['length_rate']['len_400_to_500'] += 1

            elif 500 <= _packet.packet_length < 600:
                _packet_statistics['length_rate']['len_500_to_600'] += 1

            elif 600 <= _packet.packet_length < 700:
                _packet_statistics['length_rate']['len_600_to_700'] += 1

            elif 700 <= _packet.packet_length < 800:
                _packet_statistics['length_rate']['len_700_to_800'] += 1

            elif 800 <= _packet.packet_length < 900:
                _packet_statistics['length_rate']['len_800_to_900'] += 1

            elif 900 <= _packet.packet_length < 1000:
                _packet_statistics['length_rate']['len_900_to_1000'] += 1

            elif 1000 <= _packet.packet_length < 2000:
                _packet_statistics['length_rate']['len_1000_to_2000'] += 1

            elif 2000 <= _packet.packet_length < 3000:
                _packet_statistics['length_rate']['len_2000_to_3000'] += 1

            elif 3000 <= _packet.packet_length < 4000:
                _packet_statistics['length_rate']['len_3000_to_4000'] += 1

            elif 4000 <= _packet.packet_length < 5000:
                _packet_statistics['length_rate']['len_4000_to_5000'] += 1

            elif 5000 <= _packet.packet_length < 6000:
                _packet_statistics['length_rate']['len_5000_to_6000'] += 1

            elif 6000 <= _packet.packet_length < 7000:
                _packet_statistics['length_rate']['len_6000_to_7000'] += 1

            elif 7000 <= _packet.packet_length < 8000:
                _packet_statistics['length_rate']['len_7000_to_8000'] += 1

            elif 8000 <= _packet.packet_length < 9000:
                _packet_statistics['length_rate']['len_8000_to_9000'] += 1

            elif 9000 <= _packet.packet_length < 10000:
                _packet_statistics['length_rate']['len_9000_to_10000'] += 1

            elif 10000 <= _packet.packet_length:
                _packet_statistics['length_rate']['len_10000_over'] += 1

        return _packet_statistics
