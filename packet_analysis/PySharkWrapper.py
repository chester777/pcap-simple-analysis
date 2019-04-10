import pyshark


class PySharkWrapper:
    def __init__(self, pcap_file_path):
        self._pcap_file_path = pcap_file_path

    async def result(self):
        capture = pyshark.FileCapture(self._pcap_file_path)
