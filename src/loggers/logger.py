import logging


def getLogger(name):
    logging.basicConfig(level=logging.INFO,
                        filename='log.log',
                        filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(name)
    return logger


def logInfoMsg(message, logger):
    logger.info(message)
