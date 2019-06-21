import json
import os


class ConfigParser:

    def __init__(self, config_path):
        with open(config_path, 'r') as _json_file:
            self._conf = json.load(_json_file)

    @property
    def log_path(self):
        if 'log' in self._conf:
            if 'path' in self._conf['log']:
                if (len(self._conf['log']['path']) > 0 and
                    type(self._conf['log']['path']) is str and
                    os.path.exists(self._conf['log']['path']) is True):
                    return self._conf['log']['path']
        return None

    @property
    def pcap_file_path(self):
        if 'path' in self._conf:
            if 'pcap_download' in self._conf['path']:
                return self._conf['path']['pcap_download']
        return None

    @property
    def db_path(self):
        if 'path' in self._conf:
            if 'db' in self._conf['path']:
                return self._conf['path']['db']
        return None