import os
from typing import Any, Dict, Type, Callable

from exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'VERSION'), 'rt') as f:
    __version__ = f.read().strip()

DATA_DIR = os.path.join(BASE_DIR, 'data')

empty = object()


def env(param,
        default: Any = '',
        required: bool = False,
        type_: Type = str) -> Any:
    type_rules: Dict[Type, Callable] = {
        int: int,
        bool: lambda x: x.lower() in ['true', '1', 'yes'],
        float: float,
    }
    value = os.environ.get(param, default=empty)
    if value is empty:
        if required:
            raise ImproperlyConfigured(F'{param} setting is required!')
        return default
    cast = type_rules.get(type_, str)
    return cast(value)


# Databases
DATABASE_CONNECTION_URL = env('DATABASE_CONNECTION_URL', required=True)

# App configuration
APP = {
    'host': env('APP_HOST', default='localhost'),
    'port': env('APP_PORT', default='8888', type_=int),
}
THREAD_POOL = 3
DEBUG = env('DEBUG', default=True, type_=bool)

# 3rd party services
SKYPE_CREDENTIALS = {
    'login': env('SKYPE_LOGIN'),
    'password': env('SKYPE_PASSWORD'),
}
USE_SKYPE = env('USE_SKYPE', default=False, type_=bool)

ADMINS = [
]

SKYPE_TOKEN_PATH = os.path.join(DATA_DIR, 'skype.token')
TIMEZONE = 'Europe/Minsk'
