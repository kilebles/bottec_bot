import logging

from colorama import Fore

level_log = {
    'debug': 10,
    'info': 20,
    'warning': 30,
    'error': 40,
    'exception': 50,
}

level_color = {
    'debug': Fore.WHITE,
    'info': Fore.GREEN,
    'warning': Fore.YELLOW,
    'error': Fore.MAGENTA,
    'exception': Fore.RED,
}

LOGGERS_CONFIG = [
    {'name': 'bot', 'log_level': logging.DEBUG},
]
