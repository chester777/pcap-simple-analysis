import os

from graphviz import Digraph

from commons.globals import ROOT_PATH
from commons.arg_parser import ArgParser
from commons.config_parser import ConfigParser

from commons.db_models import PacketData
from commons.sqlite_wrapper import SQLiteHelper


class PacketFlowVisualizer:

    def __init__(self):
        _arg = ArgParser()
        self._conf = ConfigParser(_arg.config_path)

        if os.path.exists(self._conf.db_dir_path) is False:
            os.makedirs(self._conf.db_dir_path)

        if os.path.exists(self._conf.image_path) is False:
            os.makedirs(self._conf.image_path)

        _db_path = '/'.join([ROOT_PATH, self._conf.db_path])
        self._db = SQLiteHelper(_db_path)

    def make_image(self, _pcap_id):
        _dot = Digraph(comment=_pcap_id, format='png')
        _result_list = self._db.session.query(PacketData).filter_by(pcap_id=_pcap_id).all()

        _nodes = list()

        for _packet in _result_list:

            _iterate_flag = False
            for _node in _nodes:
                if (_node['src'] == _packet.src_ip
                        and _node['dst'] == _packet.dst_ip):
                    if _packet.highest_protocol in _node['protocol']:
                        _node['protocol'][_packet.highest_protocol] += 1
                    else:
                        _node['protocol'][_packet.highest_protocol] = 1
                    _iterate_flag = True

            if _iterate_flag is False:
                _protocol = dict()
                _protocol[_packet.highest_protocol] = 1
                _temp_node = dict(
                    src=_packet.src_ip,
                    dst=_packet.dst_ip,
                    protocol=_protocol
                )
                _nodes.append(_temp_node)

        for _node in _nodes:
            _dot.node(_node['src'])
            _dot.node(_node['dst'])

            for _protocol, _count in _node['protocol'].items():
                _protocol_info = '%s : %s' % (_protocol, _count)
                _dot.edge(_node['src'], _node['dst'], label=_protocol_info)

        _render_path = '%s/%s' % (self._conf.image_path, _pcap_id)
        _dot.render(filename=_render_path)
        _image_path = '%s.%s' % (_render_path, 'png')
        return _image_path
