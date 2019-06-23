import threading

from commons.globals import INPUT_JOB_QUEUE, INPUT_JOB_QUEUE_LOCK
from commons.globals import OUTPUT_JOB_QUEUE, OUTPUT_JOB_QUEUE_LOCK

from packet_analysis.pyshark_wrapper import PySharkWrapper
from packet_analysis.packet_flow_visualizer import PacketFlowVisualizer

from telegram_bot.telegram_env import *


class JobWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._pcap_analyzer = PySharkWrapper()
        self._packet_visualizer = PacketFlowVisualizer()

    def run(self):
        while True:
            with INPUT_JOB_QUEUE_LOCK:
                if INPUT_JOB_QUEUE.empty() is True:
                    continue

            _job = None
            with INPUT_JOB_QUEUE_LOCK:
                _job = INPUT_JOB_QUEUE.get()

            if _job is None:
                continue

            if 'pcap_file_path' in _job:
                _pcap_id, _pcap_statistics = self._pcap_analysis(_job['pcap_file_path'])
                _image_path = self._make_image(_pcap_id)

                _pcap_statistics_text = str()

                _pcap_statistics_text += '==================================\n'
                _pcap_statistics_text += 'IP address frequency\n'
                _pcap_statistics_text += '==================================\n'

                _pcap_statistics_text += '\tsource IP:\n'
                for _src_ip, _count in _pcap_statistics['ip_frequency']['src_ip'].items():
                    _pcap_statistics_text += '\t\t%s : %s\n' % (_src_ip, _count)

                _pcap_statistics_text += '\tdestination IP:\n'
                for _dst_ip, _count in _pcap_statistics['ip_frequency']['dst_ip'].items():
                    _pcap_statistics_text += '\t\t%s : %s\n' % (_dst_ip, _count)

                _pcap_statistics_text += '\ttotal:\n'
                for _ip, _count in _pcap_statistics['ip_frequency']['total'].items():
                    _pcap_statistics_text += '\t\t%s : %s\n' % (_ip, _count)

                _pcap_statistics_text += '\n\n'

                _pcap_statistics_text += '==================================\n'
                _pcap_statistics_text += 'Highest protocol frequency\n'
                _pcap_statistics_text += '==================================\n'
                for _protocol, _count in _pcap_statistics['highest_protocol_frequency'].items():
                    _pcap_statistics_text += '\t %s : %s\n' % (_protocol, str(_count))

                _pcap_statistics_text += '\n\n'

                _pcap_statistics_text += '==================================\n'
                _pcap_statistics_text += 'Protocol frequency\n'
                _pcap_statistics_text += '==================================\n'
                for _layer in _pcap_statistics['layers_frequency']:
                    for _protocol_name, _protocol_count in _layer.items():
                        _pcap_statistics_text += '\t %s : %s\n' % (_protocol_name, str(_protocol_count))

                _pcap_statistics_text += '\n\n'

                _pcap_statistics_text += '==================================\n'
                _pcap_statistics_text += 'Packet length rate\n'
                _pcap_statistics_text += '==================================\n'
                _pcap_statistics_text += '\tlength 0 ~ 10 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_1_to_10']

                _pcap_statistics_text += '\tlength 10 ~ 100 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_10_to_100']

                _pcap_statistics_text += '\tlength 100 ~ 200 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_100_to_200']

                _pcap_statistics_text += '\tlength 200 ~ 300 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_200_to_300']

                _pcap_statistics_text += '\tlength 300 ~ 400 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_300_to_400']

                _pcap_statistics_text += '\tlength 400 ~ 500 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_400_to_500']

                _pcap_statistics_text += '\tlength 500 ~ 600 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_500_to_600']

                _pcap_statistics_text += '\tlength 600 ~ 700 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_600_to_700']

                _pcap_statistics_text += '\tlength 700 ~ 800 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_700_to_800']

                _pcap_statistics_text += '\tlength 800 ~ 900 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_800_to_900']

                _pcap_statistics_text += '\tlength 900 ~ 1000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_900_to_1000']

                _pcap_statistics_text += '\tlength 1000 ~ 2000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_1000_to_2000']

                _pcap_statistics_text += '\tlength 2000 ~ 3000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_2000_to_3000']

                _pcap_statistics_text += '\tlength 3000 ~ 4000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_3000_to_4000']

                _pcap_statistics_text += '\tlength 4000 ~ 5000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_4000_to_5000']

                _pcap_statistics_text += '\tlength 5000 ~ 6000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_5000_to_6000']

                _pcap_statistics_text += '\tlength 6000 ~ 7000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_6000_to_7000']

                _pcap_statistics_text += '\tlength 7000 ~ 8000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_7000_to_8000']

                _pcap_statistics_text += '\tlength 8000 ~ 9000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_8000_to_9000']

                _pcap_statistics_text += '\tlength 9000 ~ 10000 : %s\n' \
                                         % _pcap_statistics['length_rate']['len_9000_to_10000']

                _pcap_statistics_text += '\tlength 10000 ~ : %s\n' % _pcap_statistics['length_rate']['len_10000_over']

                _analysis_result = dict(
                    chat_id=_job['chat_id'],
                    type='packet_analysis_result',
                    pcap_statistics=_pcap_statistics_text,
                    image_path=_image_path
                )

                with OUTPUT_JOB_QUEUE_LOCK:
                    OUTPUT_JOB_QUEUE.put(_analysis_result)

            if 'cmd' in _job:
                _cmd_result = dict(
                    chat_id=_job['chat_id'],
                    type='cmd_result',
                    cmd_result=self._do_cmd(_job['cmd'])
                )

                with OUTPUT_JOB_QUEUE_LOCK:
                    OUTPUT_JOB_QUEUE.put(_cmd_result)

    def _pcap_analysis(self, pcap_file_path):
        _pcap_statistics = self._pcap_analyzer.result(pcap_file_path)
        return _pcap_statistics

    def _make_image(self, pcap_id):
        _image_path = self._packet_visualizer.make_image(pcap_id)
        return _image_path

    @staticmethod
    def _do_cmd(cmd):
        _result_text = 'null'

        if cmd == TELEGRAM_BOT_API_CMD_HELP:
            _result_text = MESSAGE_HELP

        elif cmd == TELEGRAM_BOT_API_CMD_START:
            _result_text = 'Start pcap simple analysis'

        elif cmd == TELEGRAM_BOT_API_CMD_STOP:
            _result_text = 'Stop pcap simple analysis'

        else:
            _result_text = 'Unknown command'

        return _result_text
