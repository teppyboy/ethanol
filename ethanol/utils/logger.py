import logging


__all__ = ["debug", "info", "warn", "error"]
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("ethanol")


def debug(msg, *args):
    logger.debug(msg, *args)


def info(msg, *args):
    logger.info(msg, *args)


def warn(msg, *args):
    logger.warning(msg, *args)


def error(msg, *args):
    logger.error(msg, *args)
