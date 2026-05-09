"""
frontend/services/logger.py
────────────────────────────
Logging for the desktop frontend.

Usage
-----
    from services.logger import get_logger
    log = get_logger(__name__)
"""

import logging
import logging.handlers
import sys

from config.settings import LOG_DIR, LOG_LEVEL, LOG_MAX_BYTES, LOG_BACKUP_COUNT

_COLOURS = {
    "DEBUG":    "\033[36m",
    "INFO":     "\033[32m",
    "WARNING":  "\033[33m",
    "ERROR":    "\033[31m",
    "CRITICAL": "\033[35m",
}
_RESET = "\033[0m"


class _ColourFormatter(logging.Formatter):
    FMT  = "%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s"
    DATE = "%H:%M:%S"

    def format(self, record):
        colour = _COLOURS.get(record.levelname, "")
        return f"{colour}{super().format(record)}{_RESET}"


_root_configured = False
_loggers: dict = {}


def _configure_root():
    global _root_configured
    if _root_configured:
        return

    root = logging.getLogger()
    root.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(_ColourFormatter(fmt=_ColourFormatter.FMT, datefmt=_ColourFormatter.DATE))
    root.addHandler(ch)

    fh = logging.handlers.RotatingFileHandler(
        filename=LOG_DIR / "backend.log",
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    fh.setFormatter(logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root.addHandler(fh)

    _root_configured = True


def get_logger(name: str) -> logging.Logger:
    _configure_root()
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]