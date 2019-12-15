#!/usr/bin/env python
import logging
import logging.config
import os
import yaml

from wield_services.wield.deploy.util import get_locale


def setup_logging(
        default_path=None,
        log_level=None,
):
    """
    Setup logging configuration
    """

    locale = get_locale(__file__)

    path = f'{locale.project_root}' if default_path is None else default_path

    if os.path.exists(path):
        with open(f'{path}/logging.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
    else:
        log_level = logging.INFO if log_level is None else log_level
        # logging.basicConfig(level=log_level)

    if log_level is not None:
        logger = logging.getLogger()
        logger.setLevel(log_level)

        for handler in logger.handlers:
            handler.setLevel(log_level)


if __name__ == "__main__":

    setup_logging(
        log_level=logging.DEBUG
    )

    logging.info('Configured logging')
    logging.debug('Configured logging')
    print('psyche')
