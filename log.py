import logging


def set_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger
