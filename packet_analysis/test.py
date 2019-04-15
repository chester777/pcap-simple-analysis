from packet_analysis.PySharkWrapper import PySharkWrapper
from commons.LogWrapper import LogWrapper

class Main:
    def __init__(self):
        LogWrapper('pcap-simple-analysis-logger')
        packet_analysis = PySharkWrapper()
        result = packet_analysis.result('./pcap_files/1554823444.4873579_5962_quiz0_inner.pcapng')
        print()

if __name__ == '__main__':
    Main()