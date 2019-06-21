import argparse
import os


class ArgParser:

    def __init__(self):
        self._arg_parser = argparse.ArgumentParser(
            description='Super Windows Artifact Parser'
        )
        self._set_arguments()
        self._args = self._arg_parser.parse_args()

    def _set_arguments(self):
        _config_options = self._arg_parser.add_mutually_exclusive_group()
        _config_options.required = True

        _config_options.add_argument(
            '-c', '--config',
            dest='config_path',
            action='store',
            type=str,
            default=None,
            help='Config path to want to input'
        )

    @property
    def config_path(self):
        if hasattr(self._args, 'config_path'):
            if self._args.config_path is not None:
                if os.path.isfile(self._args.config_path):
                    return self._args.config_path
        return None
