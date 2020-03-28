"""The helpers module is a collection of functions, common to other gis-tool modules."""

import logging


def setup_logging(level='INFO'):
    r"""Configures the logger Level.

    Arguments:
        level: CRITICAL -> ERROR -> WARNING -> INFO -> DEBUG.

    Side effect:
        The minimum logging level is set.
    """
    ll = logging.getLevelName(level)
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s"
        "{'file': %(filename)s 'function': %(funcName)s 'line': %(lineno)s}\n"
        "message: %(message)s\n")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(ll)