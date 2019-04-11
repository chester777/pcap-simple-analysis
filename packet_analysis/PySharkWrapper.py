import pyshark


class PySharkWrapper:
    def __init__(self):
        pass

    @staticmethod
    def result(_pcap_file_path):
        captures = pyshark.FileCapture(_pcap_file_path)
        packet_list = list()

        for capture in captures:
            packet = dict()
            packet['src_ip'] = capture.ip.src
            packet['dst_ip'] = capture.ip.dst
            packet['highest_protocol'] = capture.highest_layer
            packet['layers'] = list(_.layer_name for _ in capture.layers)
            packet['length'] = capture.length
            packet_list.append(packet)
