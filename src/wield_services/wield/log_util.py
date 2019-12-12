#!/usr/bin/env python

import logging
import os
import logging.config
import yaml


def setup_logging(
        path=None,
        default_level=None,
):
    """
    Setup logging configuration
    """
    if not path:

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(f"\ncurrent working dir: {dir_path}\n")
        path = f'{dir_path}/logging.yaml'

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
    else:
        default_level = logging.INFO if default_level is None else default_level
        logging.basicConfig(level=default_level)


if __name__ == "__main__":

    setup_logging()

    logging.info('Configured logging')
    logging.debug('Configured logging')
    print('psyche')
