import logging


__all__ = ["debug", "info", "warn", "error"]
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("ethanol")


def debug(msg, *args):
    logging.debug(msg, *args)


def info(msg, *args):
    logging.info(msg, *args)


def warn(msg, *args):
    logging.warning(msg, *args)


def error(msg, *args):
    logging.error(msg, *args)
