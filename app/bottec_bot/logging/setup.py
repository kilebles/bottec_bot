import logging
import os
import sys

from logging.handlers import RotatingFileHandler
from colorama import Style, init as colorama_init

from app.bottec_bot.logging.config import level_log, level_color, LOGGERS_CONFIG

colorama_init(autoreset=True)


def get_log_file_handler(formatter: logging.Formatter, level: str, logger_name: str) -> logging.Handler:
    folder_name = os.path.join('logs', logger_name)
    os.makedirs(folder_name, exist_ok=True)
    file_name = os.path.join(folder_name, f'{level}.log')
    handler = RotatingFileHandler(file_name, maxBytes=5 * 1024 * 1024, backupCount=3)
    handler.setLevel(level_log[level])
    handler.setFormatter(formatter)
    return handler


def configure_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for lvl in level_log:
        fmt = f'%(asctime)s [{level_color[lvl]}%(levelname)s{Style.RESET_ALL}] %(filename)s:%(lineno)d - %(message)s'
        formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')
        logger.addHandler(get_log_file_handler(formatter, lvl, name))

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s'))
    logger.addHandler(stream_handler)

    return logger


def create_loggers():
    loggers = {}
    for conf in LOGGERS_CONFIG:
        loggers[conf['name']] = configure_logger(conf['name'], conf['log_level'])
    return loggers

loggers = create_loggers()
