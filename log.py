import logging
import config


def set_logger(name):
    log_level = logging.INFO

    if config.LOG_LEVEL == "DEBUG":
        log_level = logging.DEBUG
    elif config.LOG_LEVEL == "WARNING":
        log_level = logging.WARNING
    elif config.LOG_LEVEL == "ERROR":
        log_level = logging.ERROR
    elif config.LOG_LEVEL == "CRITICAL":
        log_level = logging.CRITICAL

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    sh = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger
