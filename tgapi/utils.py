import logging
from typing import Any, Union

import requests


token_bot = ""
token_webhook = ""


def setup():
    global token_bot, token_webhook
    try:
        with open("token.txt") as f:
            token_bot = f.readline().strip()
            token_webhook = f.readline().strip()
    except Exception as e:
        logging.error(f"Cant read token\n{e}")
        raise e


def check_webhook_token(token: str):
    return token == token_webhook


def call(method: str, json: object = None, timeout: int = None):
    if timeout is not None and timeout <= 0:
        timeout = None
    r = requests.post(f"https://api.telegram.org/bot{token_bot}/{method}", json=json, timeout=timeout)
    try:
        if not r.ok:
            logging.error(f"tgapi: {method} [{r.status_code}] {json}; {r.content}")
            return False, r.json()
        return True, r.json()
    except Exception as e:
        logging.error(f"tgapi call error\n{e}")
        raise Exception("tgapi call error")


def get_all_fields(obj):
    return [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]


class ParsedJson:
    __id_field__ = None
    def __init__(self, json: dict[str, Any]):
        a = self.__annotations__
        for key in json:
            v = json[key]
            r = self._parse_field(key, v)
            if r is not None:
                key, v = r
            elif key in a:
                t = a[key]
                if isinstance(t, type) and issubclass(t, ParsedJson):
                    v = t(v)
            if hasattr(self, key):
                setattr(self, key, v)

    def _parse_field(self, key: str, v: Any) -> Union[tuple[str, Any], None]:
        return None

    def __repr__(self) -> str:
        r = self.__class__.__name__ + "("
        if self.__id_field__ is not None and hasattr(self, self.__id_field__):
            r += f"{self.__id_field__}={getattr(self, self.__id_field__)}"
        return r + ")"

    def __str__(self) -> str:
        return self.__repr__()
