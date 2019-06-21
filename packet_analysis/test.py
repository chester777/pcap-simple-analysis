from packet_analysis.pyshark_wrapper import PySharkWrapper
from commons.log_wrapper import MagicLogger
from globals import *

class Main:
    def __init__(self):
        MagicLogger(LOGGER_NAME)
        packet_analysis = PySharkWrapper()
        result = packet_analysis.result(
            _pcap_id=0,
            _pcap_file_path='./pcap_files/1554823444.4873579_5962_quiz0_inner.pcapng'
        )
        print()

if __name__ == '__main__':
    Main()